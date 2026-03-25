#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
import os
import json
import socket
import gettext
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gegl', '0.4')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gimp, GimpUi, Gegl, Gtk, Gdk, GObject, GLib
import sys

class PseudoAdjustmentLayer(Gimp.PlugIn):
    
    GIMP_OFFICIAL_MENU = [
        ("Blur", [
            ("gegl:focus-blur", "Focus Blur"),
            ("gegl:gaussian-blur", "Gaussian Blur"),
            ("gegl:lens-blur", "Lens Blur"),
            ("gegl:mean-curvature-blur", "Mean Curvature Blur"),
            ("gegl:median-blur", "Median Blur"),
            ("gegl:pixelize", "Pixelize"),
            ("gegl:selective-gaussian-blur", "Selective Gaussian Blur"),
            ("gegl:variable-blur", "Variable Blur"),
            ("gegl:motion-blur-circular", "Circular Motion Blur"),
            ("gegl:motion-blur-linear", "Linear Motion Blur"),
            ("gegl:motion-blur-zoom", "Zoom Motion Blur"),
            ("gegl:tileable-blur", "Tileable Blur")
        ]),
        ("Enhance", [
            ("gegl:antialias", "Antialias"),
            ("gegl:deinterlace", "Deinterlace"),
            ("gegl:high-pass", "High Pass"),
            ("gegl:noise-reduction", "Noise Reduction"),
            ("gegl:red-eye-removal", "Red Eye Removal"),
            ("gegl:snn-mean", "Symmetric Nearest Neighbor"),
            ("gegl:unsharp-mask", "Sharpen (Unsharp Mask)"),
            ("gegl:despeckle", "Despeckle"),
            ("gegl:nl-filter", "NL Filter")
        ]),
        ("Distorts", [
            ("gegl:apply-lens", "Apply Lens"),
            ("gegl:emboss", "Emboss"),
            ("gegl:engrave", "Engrave"),
            ("gegl:lens-distortion", "Lens Distortion"),
            ("gegl:kaleidoscope", "Kaleidoscope"),
            ("gegl:mosaic", "Mosaic"),
            ("gegl:newsprint", "Newsprint"),
            ("gegl:polar-coordinates", "Polar Coordinates"),
            ("gegl:ripple", "Ripple"),
            ("gegl:shift", "Shift"),
            ("gegl:spherize", "Spherize"),
            ("gegl:value-propagate", "Value Propagate"),
            ("gegl:video-degradation", "Video Degradation"),
            ("gegl:waves", "Waves"),
            ("gegl:whirl-pinch", "Whirl and Pinch"),
            ("gegl:wind", "Wind")
        ]),
        ("Light and Shadow", [
            ("gegl:bloom", "Bloom"),
            ("gegl:supernova", "Supernova"),
            ("gegl:lens-flare", "Lens Flare"),
            ("gegl:drop-shadow", "Drop Shadow"),
            ("gegl:long-shadow", "Long Shadow"),
            ("gegl:vignette", "Vignette")
        ]),
        ("Noise", [
            ("gegl:noise-cie-lch", "CIE lch Noise"),
            ("gegl:noise-hsv", "HSV Noise"),
            ("gegl:noise-hurl", "Hurl"),
            ("gegl:noise-pick", "Pick"),
            ("gegl:noise-rgb", "RGB Noise"),
            ("gegl:noise-slur", "Slur"),
            ("gegl:noise-spread", "Spread")
        ]),
        ("Edge-Detect", [
            ("gegl:difference-of-gaussians", "Difference of Gaussians"),
            ("gegl:edge", "Edge"),
            ("gegl:edge-laplace", "Laplace"),
            ("gegl:edge-neon", "Neon"),
            ("gegl:edge-sobel", "Sobel"),
            ("gegl:image-gradient", "Image Gradient")
        ]),
        ("Generic", [
            ("gegl:convolution-matrix", "Convolution Matrix"),
            ("gegl:distance-transform", "Distance Map"),
            ("gegl:normal-map", "Normal Map"),
            ("gegl:dilate", "Dilate"),
            ("gegl:erode", "Erode")
        ]),
        ("Combine", [
            ("gegl:depth-merge", "Depth Merge")
        ]),
        ("Artistic", [
            ("gegl:apply-canvas", "Apply Canvas"),
            ("gegl:cartoon", "Cartoon"),
            ("gegl:cubism", "Cubism"),
            ("gegl:glass-tile", "Glass Tile"),
            ("gegl:oilify", "Oilify"),
            ("gegl:photocopy", "Photocopy"),
            ("gegl:slic", "Simple Linear Iterative Clustering"),
            ("gegl:softglow", "Softglow"),
            ("gegl:waterpixels", "Waterpixels"),
            ("gegl:clothify", "Clothify"),
            ("gegl:weave", "Weave")
        ]),
        ("Decor", []),
        ("Map", [
            ("gegl:bump-map", "Bump Map"),
            ("gegl:displace", "Displace"),
            ("gegl:fractal-trace", "Fractal Trace"),
            ("gegl:illusion", "Illusion"),
            ("gegl:little-planet", "Little Planet"),
            ("gegl:panorama-projection", "Panorama Projection"),
            ("gegl:recursive-transform", "Recursive Transform"),
            ("gegl:paper-tile", "Paper Tile"),
            ("gegl:tile-seamless", "Tile Seamless")
        ]),
        ("Render", [
            ("gegl:checkerboard", "Checkerboard"),
            ("gegl:grid", "Grid"),
            ("gegl:maze", "Maze"),
            ("gegl:plasma", "Plasma"),
            ("gegl:noise-solid", "Solid Noise"),
            ("gegl:sinus", "Sinus"),
            ("gegl:noise-cell", "Cell Noise"),
            ("gegl:noise-perlin", "Perlin Noise"),
            ("gegl:noise-simplex", "Simplex Noise")
        ])
    ]

    def do_query_procedures(self):
        return ["python-pseudo-adjustment-layer"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("*")
        procedure.set_documentation("A categorized palette of available NDE filters acting as Pseudo Adjustment Layers",
                                    "Creates pseudo adjustment layers by combining NDE filters, Layer Groups, and Dummy Layers.",
                                    name)
        # メニュー名を変更
        procedure.set_menu_label("Pseudo Adjustment Layer")
        procedure.add_menu_path('<Image>/Filters/')
        return procedure

    def _gettext_translate(self, text, target_lang):
        domains = ["gimp30", "gegl-0.4", "gimp30-std-plug-ins"]
        locale_dirs = [None, "/app/share/locale", "/usr/share/locale", "/usr/local/share/locale"]
        
        search_keys = [
            text,
            text + "...",
            "filters-action\x04" + text,
            "filters-action\x04" + text + "..."
        ]
        
        for domain in domains:
            for loc_dir in locale_dirs:
                try:
                    t = gettext.translation(domain, localedir=loc_dir, languages=[target_lang])
                    for key in search_keys:
                        t_name = t.gettext(key)
                        if t_name and t_name != key:
                            if '\x04' in t_name:
                                t_name = t_name.split('\x04')[-1]
                            return t_name.replace("...", "")
                except Exception:
                    continue
        return text

    def load_or_generate_translation(self, lang_code):
        lang_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Language")
        if not os.path.exists(lang_dir):
            try:
                os.makedirs(lang_dir)
            except Exception as e:
                print("Failed to create Language directory:", e)
                
        lang_file = os.path.join(lang_dir, f"{lang_code}.json")
        
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load {lang_file}:", e)
                
        trans_data = {"categories": {}, "filters": {}}
        
        for cat_name, op_list in self.GIMP_OFFICIAL_MENU:
            local_cat = cat_name
            if not lang_code.startswith("en"):
                local_cat = self._gettext_translate(cat_name, lang_code)
                
            trans_data["categories"][cat_name] = {
                "en": cat_name,
                "local": local_cat
            }
            
            for op, en_name in op_list:
                local_name = en_name
                if not lang_code.startswith("en"):
                    local_name = self._gettext_translate(en_name, lang_code)
                    
                trans_data["filters"][op] = {
                    "en": en_name,
                    "local": local_name
                }
                
        try:
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(trans_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save {lang_file}:", e)
            
        return trans_data

    def load_favorites(self):
        if os.path.exists(self.fav_file):
            try:
                with open(self.fav_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print("Favorites load error:", e)
        return []

    def save_favorites(self):
        try:
            with open(self.fav_file, 'w') as f:
                json.dump(self.favorites, f, indent=4)
        except Exception as e:
            print("Failed to save favorites:", e)

    def load_history(self):
        if os.path.exists(self.hist_file):
            try:
                with open(self.hist_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print("History load error:", e)
        return []

    def save_history(self):
        try:
            with open(self.hist_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print("Failed to save history:", e)

    def load_config(self):
        default_config = {
            "target_lang": "ja",
            "translate_active": False,
            "auto_close": True
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print("Config load error:", e)
        return default_config

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print("Failed to save config:", e)

    def load_filter_list(self):
        if os.path.exists(self.filters_file):
            try:
                with open(self.filters_file, 'r') as f:
                    saved_list = json.load(f)
                    valid_ops = {op for cat, ops in self.GIMP_OFFICIAL_MENU for op, name in ops}
                    return [f for f in saved_list if f in valid_ops]
            except Exception as e:
                print("Filters load error:", e)
        return self.fetch_and_save_filters()

    def fetch_and_save_filters(self):
        ops = Gegl.list_operations()
        gegl_ops = set(ops)
        filters = []
        
        for cat_name, op_list in self.GIMP_OFFICIAL_MENU:
            for op, _ in op_list:
                if op in gegl_ops:
                    filters.append(op)
                    
        self.save_filter_list(filters)
        return filters

    def save_filter_list(self, filters):
        try:
            with open(self.filters_file, 'w') as f:
                json.dump(filters, f, indent=4)
        except Exception as e:
            print("Failed to save filters:", e)

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())

        self.lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.lock_socket.bind(("127.0.0.1", 54321))
        except socket.error:
            print("Pseudo Adjustment Layer is already running.")
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        self.image = image
        self.drawable = drawables[0]
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 新しい名前に合わせてファイル名を一新
        self.fav_file = os.path.join(base_dir, "pal_favorites.json")
        self.hist_file = os.path.join(base_dir, "pal_history.json")
        self.filters_file = os.path.join(base_dir, "pal_filters.json")
        self.config_file = os.path.join(base_dir, "pal_config.json")
        
        self.favorites = self.load_favorites()
        self.history = self.load_history()
        self.available_filters = self.load_filter_list()
        self.config = self.load_config()
        
        self.current_translation = self.load_or_generate_translation(self.config.get("target_lang", "ja"))

        GimpUi.init("python-pseudo-adjustment-layer")
        Gegl.init(None)

        # ウィンドウのタイトルを変更
        self.window = Gtk.Window(title="Pseudo Adjustment Layer")
        self.window.set_default_size(350, 600)
        self.window.set_position(Gtk.WindowPosition.MOUSE)
        self.window.set_keep_above(True)
        self.window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.window.connect("destroy", Gtk.main_quit)

        try:
            GimpUi.window_set_transient(self.window)
        except Exception as e:
            print(f"Transient Error: {e}")

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_vbox.set_border_width(10)
        self.window.add(main_vbox)

        switch_trans_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        switch_trans_label = Gtk.Label(label="Translate filter names")
        switch_trans_box.pack_start(switch_trans_label, False, False, 0)
        
        right_trans_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        
        self.btn_lang = Gtk.Button(label="🌐 Select")
        self.btn_lang.connect("clicked", self.on_select_language_clicked)
        self.btn_lang.set_valign(Gtk.Align.CENTER)
        right_trans_box.pack_start(self.btn_lang, False, False, 0)
        
        self.switch_translate = Gtk.Switch()
        self.switch_translate.set_active(self.config.get("translate_active", False))
        self.switch_translate.set_valign(Gtk.Align.CENTER)
        self.switch_translate.connect("notify::active", self.on_translate_toggled)
        right_trans_box.pack_start(self.switch_translate, False, False, 0)
        
        switch_trans_box.pack_end(right_trans_box, False, False, 0)
        main_vbox.pack_start(switch_trans_box, False, False, 0)

        switch_close_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        switch_close_label = Gtk.Label(label="Auto-close on apply")
        switch_close_box.pack_start(switch_close_label, False, False, 0)
        
        self.switch_close = Gtk.Switch()
        self.switch_close.set_active(self.config.get("auto_close", True))
        self.switch_close.set_valign(Gtk.Align.CENTER)
        self.switch_close.connect("notify::active", self.on_autoclose_toggled)
        switch_close_box.pack_end(self.switch_close, False, False, 0)
        
        main_vbox.pack_start(switch_close_box, False, False, 0)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search filters...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        main_vbox.pack_start(self.search_entry, False, False, 0)

        self.store = Gtk.TreeStore(str, str)
        self.filter_model = self.store.filter_new()
        self.filter_model.set_visible_func(self.filter_tree_visible)

        self.treeview = Gtk.TreeView(model=self.filter_model)
        self.treeview.set_headers_visible(False)
        self.treeview.connect("cursor-changed", self.on_tree_selection_changed)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-press-event", self.on_tree_button_press)
        
        self.treeview.connect("row-expanded", self.on_row_expanded)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Filter", renderer, text=0)
        self.treeview.append_column(column)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.treeview)
        main_vbox.pack_start(scroll, True, True, 0)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.btn_reset_filters = Gtk.Button(label="🔄 Reset List")
        self.btn_reset_filters.connect("clicked", self.on_reset_filters_clicked)
        btn_box.pack_start(self.btn_reset_filters, True, True, 0)
        
        main_vbox.pack_start(btn_box, False, False, 0)

        self.selected_op_name = None
        self.search_query = ""

        self.populate_tree()
        
        self.window.show_all()
        Gtk.main()
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def on_row_expanded(self, treeview, iter, path):
        if self.search_query:
            return
        model = treeview.get_model()
        current_iter = model.get_iter_first()
        while current_iter is not None:
            current_path = model.get_path(current_iter)
            if current_path.get_indices()[0] != path.get_indices()[0]:
                treeview.collapse_row(current_path)
            current_iter = model.iter_next(current_iter)

    def on_select_language_clicked(self, widget):
        dialog = Gtk.Dialog(
            title="Select Translation Language",
            transient_for=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.set_default_size(300, 450)

        lang_list = [
            ("ar", "Arabic (العربية)"), ("ast", "Asturian (Asturianu)"), ("az", "Azerbaijani (Azərbaycan)"),
            ("be", "Belarusian (Беларуская)"), ("bg", "Bulgarian (Български)"), ("br", "Breton (Brezhoneg)"),
            ("bs", "Bosnian (Bosanski)"), ("ca", "Catalan (Català)"), ("ca@valencia", "Catalan - Valencian (Català - Valencià)"),
            ("cs", "Czech (Čeština)"), ("da", "Danish (Dansk)"), ("de", "German (Deutsch)"), ("dz", "Dzongkha (རྫོང་-ཁ)"),
            ("el", "Greek (Ελληνικά)"), ("en_CA", "English - Canadian"), ("en_GB", "English - British"),
            ("eo", "Esperanto"), ("es", "Spanish (Español)"), ("et", "Estonian (Eesti)"), ("eu", "Basque (Euskara)"),
            ("fa", "Persian (فارسی)"), ("fi", "Finnish (Suomi)"), ("fr", "French (Français)"), ("ga", "Irish (Gaeilge)"),
            ("gl", "Galician (Galego)"), ("gu", "Gujarati (ગુજરાતી)"), ("he", "Hebrew (עברית)"), ("hi", "Hindi (हिन्दी)"),
            ("hr", "Croatian (Hrvatski)"), ("hu", "Hungarian (Magyar)"), ("id", "Indonesian (Bahasa Indonesia)"),
            ("is", "Icelandic (Íslenska)"), ("it", "Italian (Italiano)"), ("ja", "Japanese (日本語)"),
            ("ka", "Georgian (ქართული)"), ("kab", "Kabyle (Taqbaylit)"), ("kk", "Kazakh (Қазақ)"),
            ("km", "Khmer (ខ្មែរ)"), ("kn", "Kannada (ಕನ್ನಡ)"), ("ko", "Korean (한국어)"),
            ("lt", "Lithuanian (Lietuvių)"), ("lv", "Latvian (Latviešu)"), ("mk", "Macedonian (Македонски)"),
            ("mr", "Marathi (मराठी)"), ("ms", "Malay (Bahasa Melayu)"), ("my", "Burmese (မြန်မာစာ)"),
            ("nb", "Norwegian Bokmål (Norsk bokmål)"), ("ne", "Nepali (नेपाली)"), ("nl", "Dutch (Nederlands)"),
            ("nn", "Norwegian Nynorsk (Norsk nynorsk)"), ("oc", "Occitan (Occitan)"), ("pa", "Punjabi (ਪੰਜਾਬੀ)"),
            ("pl", "Polish (Polski)"), ("pt", "Portuguese (Português)"), ("pt_BR", "Portuguese - Brazilian (Português do Brasil)"),
            ("ro", "Romanian (Română)"), ("ru", "Russian (Русский)"), ("rw", "Kinyarwanda (Ikinyarwanda)"),
            ("sk", "Slovak (Slovenčina)"), ("sl", "Slovenian (Slovenščina)"), ("sr", "Serbian (Српски)"),
            ("sr@latin", "Serbian - Latin (Srpski - latinica)"), ("sv", "Swedish (Svenska)"),
            ("ta", "Tamil (தமிழ்)"), ("te", "Telugu (తెలుగు)"), ("th", "Thai (ไทย)"), ("tr", "Turkish (Türkçe)"),
            ("uk", "Ukrainian (Українська)"), ("vi", "Vietnamese (Tiếng Việt)"), ("zh_CN", "Chinese Simplified (简体中文)"),
            ("zh_HK", "Chinese Hong Kong (繁體中文 - 香港)"), ("zh_TW", "Chinese Traditional (繁體中文 - 台灣)")
        ]

        store = Gtk.ListStore(str, str)
        for code, name in lang_list:
            store.append([code, name])

        tree = Gtk.TreeView(model=store)
        tree.set_headers_visible(False)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Language", renderer, text=1)
        tree.append_column(column)

        current_lang = self.config.get("target_lang", "ja")
        for i, (code, name) in enumerate(lang_list):
            if code == current_lang:
                tree.set_cursor(Gtk.TreePath.new_from_indices([i]), None, False)
                break

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(tree)
        
        box = dialog.get_content_area()
        box.pack_start(scroll, True, True, 0)
        box.show_all()
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selection = tree.get_selection()
            model, treeiter = selection.get_selected()
            if treeiter is not None:
                selected_code = model.get_value(treeiter, 0)
                self.config["target_lang"] = selected_code
                self.save_config()
                self.current_translation = self.load_or_generate_translation(selected_code)
                
                if self.switch_translate.get_active():
                    self.refresh_tree()
                    
        dialog.destroy()

    def get_translated_category(self, cat_name):
        if cat_name in self.current_translation.get("categories", {}):
            return self.current_translation["categories"][cat_name].get("local", cat_name)
        return cat_name

    def get_display_name_from_tuple(self, op_name, default_eng_name, translate=False):
        if not translate:
            if op_name in self.current_translation.get("filters", {}):
                return self.current_translation["filters"][op_name].get("en", default_eng_name)
            return default_eng_name

        if op_name in self.current_translation.get("filters", {}):
            return self.current_translation["filters"][op_name].get("local", default_eng_name)
        return default_eng_name

    def on_translate_toggled(self, switch, gparam):
        self.config["translate_active"] = switch.get_active()
        self.save_config()
        self.refresh_tree()

    def on_autoclose_toggled(self, switch, gparam):
        self.config["auto_close"] = switch.get_active()
        self.save_config()

    def get_op_name_for_dialog(self, actual_op):
        translate_active = self.switch_translate.get_active()
        for cat, ops in self.GIMP_OFFICIAL_MENU:
            for op, eng_name in ops:
                if op == actual_op:
                    return self.get_display_name_from_tuple(op, eng_name, translate_active)
        eng_name = actual_op.replace("gegl:", "").replace("gimp:", "").replace("-", " ").title()
        return self.get_display_name_from_tuple(actual_op, eng_name, translate_active)

    def populate_tree(self):
        self.store.clear()

        available_set = set(self.available_filters)
        translate_active = self.switch_translate.get_active()

        fav_iter = self.store.append(None, ["⭐ Favorites", ""])
        if self.favorites:
            for op in self.favorites:
                if op in available_set:
                    disp_name = self.get_op_name_for_dialog(op)
                    self.store.append(fav_iter, [f"    {disp_name}", op])

        hist_iter = self.store.append(None, ["📝 History", ""])
        if self.history:
            for op in self.history:
                if op in available_set:
                    disp_name = self.get_op_name_for_dialog(op)
                    self.store.append(hist_iter, [f"    {disp_name}", op])

        placed_ops = set()

        for cat_name, ops in self.GIMP_OFFICIAL_MENU:
            active_ops = [op_tuple for op_tuple in ops if op_tuple[0] in available_set]
            if not active_ops:
                continue
                
            cat_disp_name = cat_name
            if translate_active:
                cat_disp_name = self.get_translated_category(cat_name)
                
            parent_iter = self.store.append(None, [f"🗃️ {cat_disp_name}", ""])
            
            for op, default_eng_name in active_ops:
                disp_name = self.get_display_name_from_tuple(op, default_eng_name, translate_active)
                self.store.append(parent_iter, [f"    {disp_name}", op])
                placed_ops.add(op)
                
        orphans = [op for op in self.available_filters if op not in placed_ops]
        if orphans:
            cat_disp_name = "Generic"
            if translate_active:
                cat_disp_name = self.get_translated_category("Generic")
            parent_iter = self.store.append(None, [f"🗃️ {cat_disp_name}", ""])
            
            for op in sorted(orphans):
                disp_name = self.get_op_name_for_dialog(op)
                self.store.append(parent_iter, [f"    {disp_name}", op])

    def refresh_tree(self):
        expanded_name = None
        
        if not self.search_query:
            model = self.filter_model
            current_iter = model.get_iter_first()
            while current_iter is not None:
                path = model.get_path(current_iter)
                if self.treeview.row_expanded(path):
                    expanded_name = model.get_value(current_iter, 0)
                    break
                current_iter = model.iter_next(current_iter)

        self.populate_tree()
        self.filter_model.refilter()

        if expanded_name and not self.search_query:
            model = self.filter_model
            current_iter = model.get_iter_first()
            while current_iter is not None:
                if model.get_value(current_iter, 0) == expanded_name:
                    self.treeview.expand_row(model.get_path(current_iter), False)
                    break
                current_iter = model.iter_next(current_iter)

    def on_reset_filters_clicked(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Reset, Validate & Reload?"
        )
        dialog.format_secondary_text(
            "This will perform the following:\n"
            "1. Fetch the official GIMP filter list.\n"
            "2. Validate compatibility of all filters.\n"
            "3. Reload your translation JSON file.\n\n"
            "It may take a few seconds. Do you want to proceed?"
        )
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            raw_filters = self.fetch_and_save_filters()
            
            valid_filters = []
            temp_image = Gimp.Image.new(10, 10, Gimp.ImageBaseType.RGB)
            
            for op in raw_filters:
                temp_group = None
                try:
                    temp_group = Gimp.GroupLayer.new(temp_image)
                    temp_image.insert_layer(temp_group, None, 0)
                    
                    temp_dummy = Gimp.Layer.new(
                        temp_image, "DUMMY", 10, 10,
                        Gimp.ImageType.RGBA_IMAGE, 100.0, Gimp.LayerMode.NORMAL
                    )
                    temp_dummy.fill(getattr(Gimp.FillType, 'TRANSPARENT', 3))
                    temp_image.insert_layer(temp_dummy, temp_group, 0)
                    
                    test_node = Gimp.DrawableFilter.new(temp_group, op, op)
                    temp_group.append_filter(test_node)
                    
                    applied_filters = temp_group.get_filters()
                    if applied_filters and len(applied_filters) > 0:
                        valid_filters.append(op)
                    
                except Exception:
                    pass
                finally:
                    if temp_group is not None and temp_group.is_valid():
                        try:
                            temp_image.remove_layer(temp_group)
                        except Exception:
                            pass
            
            temp_image.delete()
            
            removed_count = len(raw_filters) - len(valid_filters)
            self.available_filters = valid_filters
            self.save_filter_list(self.available_filters)
            
            original_fav_count = len(self.favorites)
            self.favorites = [f for f in self.favorites if f in valid_filters]
            if len(self.favorites) < original_fav_count:
                self.save_favorites()

            original_hist_count = len(self.history)
            self.history = [f for f in self.history if f in valid_filters]
            if len(self.history) < original_hist_count:
                self.save_history()

            target_lang = self.config.get("target_lang", "ja")
            self.current_translation = self.load_or_generate_translation(target_lang)

            self.refresh_tree()
            
            info_dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Process Complete"
            )
            info_dialog.format_secondary_text(
                f"Validation and translation reload finished.\n"
                f"{removed_count} incompatible filter(s) were removed."
            )
            info_dialog.run()
            info_dialog.destroy()

    def on_tree_button_press(self, treeview, event):
        if event.button == 3:
            path_info = treeview.get_path_at_pos(int(event.x), int(event.y))
            if path_info is not None:
                path, col, cell_x, cell_y = path_info
                treeview.set_cursor(path, col, 0)
                
                model, treeiter = treeview.get_selection().get_selected()
                if treeiter is not None:
                    actual_op = model.get_value(treeiter, 1)
                    if actual_op != "":
                        self.show_context_menu(event, actual_op)
            return True
        return False

    def show_context_menu(self, event, actual_op):
        menu = Gtk.Menu()
        
        if actual_op in self.favorites:
            item_fav = Gtk.MenuItem(label="❌ Remove from Favorites")
            item_fav.connect("activate", self.on_remove_favorite, actual_op)
        else:
            item_fav = Gtk.MenuItem(label="⭐ Add to Favorites")
            item_fav.connect("activate", self.on_add_favorite, actual_op)
            
        menu.append(item_fav)
        menu.append(Gtk.SeparatorMenuItem())
        
        item_delete = Gtk.MenuItem(label="🗑️ Remove from List")
        item_delete.connect("activate", self.on_remove_from_list, actual_op)
        menu.append(item_delete)
        
        menu.show_all()
        menu.popup_at_pointer(event)

    def on_add_favorite(self, widget, actual_op):
        if actual_op not in self.favorites:
            self.favorites.append(actual_op)
            self.save_favorites()
            self.refresh_tree()
            
            def expand_favorites(model, path, iter, data):
                if model.get_value(iter, 0) == "⭐ Favorites":
                    self.treeview.expand_row(path, False)
            self.filter_model.foreach(expand_favorites, None)

    def on_remove_favorite(self, widget, actual_op):
        if actual_op in self.favorites:
            self.favorites.remove(actual_op)
            self.save_favorites()
            self.refresh_tree()

    def on_remove_from_list(self, widget, actual_op):
        display_name = self.get_op_name_for_dialog(actual_op)
        
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Remove Filter from List?"
        )
        dialog.format_secondary_text(
            f"Are you sure you want to completely remove '{display_name}' from the filter palette?\n\n"
            "You can restore it later by clicking the 'Reset List, Validate & Reload' button at the bottom."
        )
        
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            if actual_op in self.available_filters:
                self.available_filters.remove(actual_op)
                self.save_filter_list(self.available_filters)
                
            if actual_op in self.favorites:
                self.favorites.remove(actual_op)
                self.save_favorites()

            if actual_op in self.history:
                self.history.remove(actual_op)
                self.save_history()
                
            self.refresh_tree()

    def on_search_changed(self, search_entry):
        self.search_query = search_entry.get_text().lower()
        self.filter_model.refilter()
        
        if self.search_query:
            self.treeview.expand_all()
        else:
            self.treeview.collapse_all()

    def filter_tree_visible(self, model, iter, data):
        if not self.search_query:
            return True

        disp_name_raw = model.get_value(iter, 0)
        
        if disp_name_raw.startswith("⭐") or disp_name_raw.startswith("📝"):
            return False
            
        parent_iter = model.iter_parent(iter)
        if parent_iter is not None:
            parent_name = model.get_value(parent_iter, 0)
            if parent_name.startswith("⭐") or parent_name.startswith("📝"):
                return False

        disp_name = disp_name_raw.lower()
        actual_op = model.get_value(iter, 1).lower()

        if actual_op == "":
            child_iter = model.iter_children(iter)
            while child_iter:
                child_disp = model.get_value(child_iter, 0).lower()
                child_op = model.get_value(child_iter, 1).lower()
                if self.search_query in child_disp or self.search_query in child_op:
                    return True
                child_iter = model.iter_next(child_iter)
            return self.search_query in disp_name

        return self.search_query in disp_name or self.search_query in actual_op

    def on_tree_selection_changed(self, treeview):
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()
        
        if treeiter is not None:
            actual_op = model.get_value(treeiter, 1)
            if actual_op != "":
                self.selected_op_name = actual_op
                return
                
        self.selected_op_name = None

    def on_row_activated(self, treeview, path, column):
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            actual_op = model.get_value(treeiter, 1)
            if actual_op != "":
                self.selected_op_name = actual_op
                self.apply_filter(None)
            else:
                if treeview.row_expanded(path):
                    treeview.collapse_row(path)
                else:
                    treeview.expand_row(path, False)

    def apply_filter(self, widget):
        if not self.selected_op_name: return

        active_drawables = self.image.get_selected_drawables()
        if not active_drawables: return
        target_drawable = active_drawables[0]

        display_name = self.selected_op_name
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            display_name = model.get_value(treeiter, 0).strip()

        self.image.undo_group_start()

        parent = target_drawable.get_parent()
        position = self.image.get_item_position(target_drawable)

        group = Gimp.GroupLayer.new(self.image)
        group.set_name(f"fx: {display_name}")
        group.set_mode(Gimp.LayerMode.PASS_THROUGH)
        self.image.insert_layer(group, parent, position)

        dummy_layer = Gimp.Layer.new(
            self.image,
            "DUMMY",
            self.image.get_width(),
            self.image.get_height(),
            Gimp.ImageType.RGBA_IMAGE,
            100.0,
            Gimp.LayerMode.NORMAL
        )
        dummy_layer.fill(getattr(Gimp.FillType, 'TRANSPARENT', 3))
        self.image.insert_layer(dummy_layer, group, 0)
        
        try:
            def _unwrap(v):
                if hasattr(v, 'get_enum'): return v.get_enum()
                if hasattr(v, 'get_boolean'): return v.get_boolean()
                if hasattr(v, 'get_value'): return v.get_value()
                return v

            proc_is_empty = Gimp.get_pdb().lookup_procedure('gimp-selection-is-empty')
            config_is_empty = proc_is_empty.create_config()
            config_is_empty.set_property('image', self.image)
            res_empty = proc_is_empty.run(config_is_empty)
            
            if _unwrap(res_empty.index(0)) == Gimp.PDBStatusType.SUCCESS:
                is_empty = _unwrap(res_empty.index(1))
                
                if not is_empty:
                    mask_type = getattr(Gimp.AddMaskType, 'SELECTION', 4)
                    mask = group.create_mask(mask_type)
                    group.add_mask(mask)
                    
                    proc_none = Gimp.get_pdb().lookup_procedure('gimp-selection-none')
                    config_none = proc_none.create_config()
                    config_none.set_property('image', self.image)
                    proc_none.run(config_none)
        except Exception as e:
            print(f"Mask Error: {e}")

        try:
            filter_node = Gimp.DrawableFilter.new(group, self.selected_op_name, display_name)
            group.append_filter(filter_node)
            
            applied_filters = group.get_filters()
            if not applied_filters or len(applied_filters) == 0:
                raise Exception("Silently rejected by GIMP")
                
        except Exception:
            self.image.remove_layer(group)
            self.image.undo_group_end()
            
            if self.selected_op_name in self.available_filters:
                self.available_filters.remove(self.selected_op_name)
                self.save_filter_list(self.available_filters)
            if self.selected_op_name in self.favorites:
                self.favorites.remove(self.selected_op_name)
                self.save_favorites()
            if self.selected_op_name in self.history:
                self.history.remove(self.selected_op_name)
                self.save_history()
            self.refresh_tree()
            
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=Gtk.DialogFlags.MODAL,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Filter Application Error"
            )
            dialog.format_secondary_text(f"'{display_name}' cannot be applied as a non-destructive filter. It has been removed from the list.")
            dialog.run()
            dialog.destroy()
            return
        
        try:
            group.set_expanded(False)
        except Exception:
            pass
            
        if self.selected_op_name in self.history:
            self.history.remove(self.selected_op_name)
        self.history.insert(0, self.selected_op_name)
        self.history = self.history[:10]
        self.save_history()

        self.image.undo_group_end()
        Gimp.displays_flush()
        
        if self.switch_close.get_active():
            Gtk.main_quit()
        else:
            self.refresh_tree()

if __name__ == '__main__':
    Gimp.main(PseudoAdjustmentLayer.__gtype__, sys.argv)