#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

#a============================================================================
#a                                   المشروع : برنامج تسمية عدة ملفات دفعة واحدة  
#a                                <asmaaarab@gmail.com>    المطور  :  أحمد رغدي 
#a  http://www.ojuba.org/wiki/doku.php/waqf/license  الرخصة  : رخصة وقف العامة
#a============================================================================

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango
from os.path import join, dirname, realpath, exists, splitext, basename, isdir, expanduser
from os import rename
import re

Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
PATH0 = dirname(realpath(__file__))

ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
ACCEL_SHFT_KEY, ACCEL_SHFT_MOD = Gtk.accelerator_parse("<Shift>")
ACCEL_ALT_KEY, ACCEL_ALT_MOD = Gtk.accelerator_parse("<Alt>")

SOWAR_ALQURAN = [["AlFatihah","الفاتحة"],["AlBaqarah ","البقرة"],["Al'Imran","آل عمران"],["AnNisa'","النساء"],["AlMa'idah","المائدة"]
                 ,["AlAn'am","الأنعام"],["AlA'raf","الأعراف"],["AlAnfal","الأنفال"],["AtTaubah","التوبة"],["Yunus","يونس"],["Hud","هود"]
                 ,["Yusuf","يوسف"],["ArRa'd","الرعد"],["Ibrahim","إبراهيم"],["AlHijr","الحجر"],["AnNahl","النحل"],["AlIsra'","الإسراء"]
                 ,["AlKahf","الكهف"],["Maryam","مريم"],["TaHa","طه"],["AlAnbiya'","الأنبياء"],["AlHajj","الحج"],["AlMu'minun","المؤمنون"]
                 ,["AnNur","النور"],["AlFurqan","الفرقان"],["AshShu'ara'","الشعراء"],["AnNaml","النمل"],["AlQasas","القصص"]
                 ,["AlAnkabut","العنكبوت"],["ArRum","الروم"],["Luqman","لقمان"],["AsSajdah","السجدة"],["AlAhzab","الأحزاب"]
                 ,["Saba'","سبأ"],["Fatir","فاطر"],["YaSin","يس"],["AsSaffat","الصافات"],["Sad","ص"],["AzZumar","الزمر"],["Ghafir","غافر"]
                 ,["Fussilat","فصلت"],["AshShura","الشورى"],["AzZukhruf","الزخرف"],["AdDukhan","الدخان"],["AlJathiyah","الجاثية"]
                 ,["AlAhqaf","الأحقاف"],["Muhammad","محمد"],["AlFath","الفتح"],["AlHujurat","الحجرات"],["Qaf","ق"]
                 ,["AdhDhariyat","الذاريات"],["AtTur","الطور"],["AnNajm","النجم"],["Qamar","القمر"],["ArRahman","الرحمن"],["AlWaqi'ah","الواقعة"]
                 ,["AlHadid","الحديد"],["AlMujadilah","المجادلة"],["AlHashr","الحشر"],["AlMumtahanah","الممتحنة"],["AsSaff","الصف"]
                 ,["AlJumu'ah","الجمعة"],["AlMunafiqun","المنافقون"],["AtTaghabun","التغابن"],["AtTalaq","الطلاق"],["AtTahrim","التحريم"]
                 ,["AlMulk","الملك"],["AlQalam","القلم"],["AlHaqqah","الحاقة"],["AlMa'arij","المعارج"],["Nuh","نوح"],["AlJinn","الجن"]
                 ,["AlMuzzammil","المزمل"],["AlMuddaththir","المدثر"],["AlQiyamah","القيامة"],["AlInsan","الإنسان"],["AlMursalat","المرسلات"]
                 ,["AnNaba'","النبأ"],["AnNazi'at","النازعات"],["Abasa","عبس"],["AtTakwir","التكوير"],["AlInfitar","الانفطار"],["AlMutaffifin","المطففين"]
                 ,["AlInshiqaq","الانشقاق"],["AlBuruj","البروج"],["AtTariq","الطارق"],["AlA'la","الأعلى"],["AlGhashiyah","الغاشية"],["AlFajr","الفجر"]
                 ,["AlBalad","البلد"],["AshShams","الشمس"],["AlLail","الليل"],["AdDuha","الضحى"],["AshSharh","الشرح"],["AtTin","التين"]
                 ,["AlAlaq","العلق"],["AlQadr","القدر"],["AlBayyinah","البينة"],["AzZalzalah","الزلزلة"],["AlAadiyat","العاديات"],["AlQari'ah","القارعة"]
                 ,["AtTakathur","التكاثر"],["AlAsr","العصر"],["AlHumazah","الهمزة"],["AlFil","الفيل"],["Quraish","قريش"],["AlMa'un","الماعون"]
                 ,["AlKauthar","الكوثر"],["AlKafirun","الكافرون"],["AnNasr","النصر"],["AlMasad","المسد"],["AlIkhlas","الإخلاص"],["AlFalaq","الفلق"]
                 ,["AnNas","الناس"]]

LETTERS_HIDJAI = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي' ]
LETTERS_ABJADI = ['ا', 'ب', 'ج', 'د', 'ه', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل', 'م', 'ن', 'س', 'ع', 'ف', 'ص', 'ق', 'ر', 'ش', 'ت', 'ث', 'خ', 'ذ', 'ض', 'ظ', 'غ' ]
LETTERS_LATIN = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
NOMBER_N = {'0':'٠', '1':'١', '2':'٢', '3':'٣', '4':'٤', '5':'٥‌', '6':'٦', '7':'٧', '8':'٨', '9':'٩'}
#NOMBER_N = {'٠':'0', '١':'1', '٢':'2', '٣':'3', '٤':'4', '٥‌':'5', '٦':'6', '٧':'7', '٨':'8', '٩':'9'}
NAME_ORDINAL_ONE = {0:'o',1:'الحادي',2:'الثاني',3:'الثالث',4:'الرابع',5:'الخامس',6:'السادس',7:'السابع',8:'الثامن',9:'التاسع'}
NAME_ORDINAL_TEN = {0:'o',1:'عشر',2:'العشرون',3:'الثلاثون',4:'الأربعون',5:'الخمسون',6:'الستون',7:'السبعون',8:'الثمانون',9:'التسعون'}
NAME_ORDINAL_hundred = {0:'o',1:'المائة',2:'المائتان',3:'الثلاثمائة',4:'الأربعمائة',5:'الخمسمائة',6:'الستمائة',7:'السبعمائة',8:'الثمانمائة',9:'التسعمائة'}

list_anw3 = [
         (r'النص المضاف', [r'', r''])
         ,(r'أول رقم', [r'مغربية', r'مشرقية'])
         ,(r'أول حرف', [r'هجائية', r'أبجدية'])
         ,(r'أول حرف', [r'صغيرة', r'كبيرة'])
         ,( r'أول مرتبة(رقم)', [r'مذكرة', r'مؤنثة'])
         ,(r'أول سورة', [r'عربية', r'انكليزية'])]

#a------------------------------------------
def info(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def erro(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def sure(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
    dlg.set_markup(msg)                         
    r = dlg.run()
    dlg.destroy()
    return r

class RenameAll(Gtk.Window): 
    
    def __init__(self, *a):
        Gtk.Window.__init__(self)
        self.axl = Gtk.AccelGroup()
        self.add_accel_group(self.axl)
        self.connect("delete_event", Gtk.main_quit)
        self.connect("destroy", Gtk.main_quit)
        self.path_last = expanduser('~/')
        self.build()
        
    def start_rename(self, *a):
        if len(self.store_files) == 0: return
        res = sure(self, 'هل تريد إعادة تسمية هذه الملفات؟')
        if res == -8:
            s = len(self.store_files)-1
            while s >= 0:
                iter0 = self.store_files.get_iter(s)
                old_name = self.store_files.get_value(iter0, 3)
                new_name = join(dirname(old_name), self.store_files.get_value(iter0, 2))
                if self.store_files.get_value(iter0, 0):
                    if exists(new_name) and new_name != old_name:
                        for b in range(1000):
                            new_name0 = dirname(new_name)+'/'+str(b)+'_'+basename(new_name)
                            if not exists(new_name0):
                                new_name = new_name0
                                break
                    if new_name != old_name: rename(old_name, new_name)
                    self.store_files.remove(iter0)
                s -= 1
            info(self, 'تم تسمية جميع الملفات المراد إعادة تسميتها')
    
    def move_file(self, v):
        model, i = self.sel_files.get_selected()
        if i:
            if v == 1:
                i0 = model.iter_next(i)
                model.move_after(i, i0)
            if v == -1:
                i0 = model.iter_previous(i)
                model.move_before(i, i0)
        self.change_new_name()
        
    def move_option(self, v):
        model, i = self.sel_option.get_selected()
        if i:
            if v == 1:
                ls = eval(model.get_value(i, 0))
                if ls[0] == 'new':
                    erro(self, 'لا يمكن إنزال هذه العملية إلى أسفل')
                else:
                    i0 = model.iter_next(i)
                    model.move_after(i, i0)
            if v == -1:
                i0 = model.iter_previous(i)
                ls = eval(model.get_value(i0, 0))
                if ls[0] == 'new':
                    erro(self, 'لا يمكن رفع هذه العملية إلى أعلى')
                else: model.move_before(i, i0)
        self.change_new_name()
    
    def remove_file(self, *a):
        model, i = self.sel_files.get_selected()
        if i:
            msg = sure(self, 'سيتم حذف هذا الملف')
            if msg == Gtk.ResponseType.YES:
                model.remove(i)
                self.change_new_name()
    
    def remove_files(self, *a):
        if len(self.store_files) > 0:
            msg = sure(self, 'سيتم حذف جميع الملفات')
            if msg == Gtk.ResponseType.YES:
                self.store_files.clear()
                
    def remove_option(self, *a):
        model, i = self.sel_option.get_selected()
        if i:
            msg = sure(self, 'سيتم حذف هذا العملية')
            if msg == Gtk.ResponseType.YES:
                model.remove(i)
                self.change_new_name()
    
    def remove_options(self, *a):
        if len(self.store_option) > 0:
            msg = sure(self, 'سيتم حذف جميع العمليات')
            if msg == Gtk.ResponseType.YES:
                self.store_option.clear()
                self.change_new_name()
    
    def add_files_cb(self, *a):
        add_dlg = Gtk.FileChooserDialog("اختر ملفات للتسمية", self, 
                                      buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
        cl_button = add_dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        add_dlg.set_filename(self.path_last)
        def cll(widget,*a):
            for i in add_dlg.get_filenames():
                if isdir(i): continue
                self.store_files.append([True, basename(i), basename(i), i])
                self.path_last = i
        cl_button.connect('clicked',cll)
        add_dlg.set_select_multiple(True)
        add_dlg.run()
        add_dlg.destroy()
        self.change_new_name()
        
    def add_folders_cb(self, *a):
        add_dlg = Gtk.FileChooserDialog("اختر مجلدات للتسمية", self, 
                                      Gtk.FileChooserAction.SELECT_FOLDER,
                                      buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
        cl_button = add_dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        add_dlg.set_filename(self.path_last)
        def cll(widget,*a):
            for i in add_dlg.get_filenames():
                self.store_files.append([True, basename(i), basename(i), i])
                self.path_last = i
        cl_button.connect('clicked',cll)
        add_dlg.set_select_multiple(True)
        add_dlg.run()
        add_dlg.destroy()
        self.change_new_name()
    
    def fixed_toggled_field(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 0)
        fixed = not fixed
        model.set(itr, 0, fixed)
        
    def split_ext(self, file_path, file_name):
        if not isdir(file_path): filename, extension = splitext(file_name)
        else: filename, extension = file_name, ''
        return filename, extension
    
    def add_new_name_cb(self, *a):
        text = self.entry_new_name.get_text()
        if text != '':
            if len(self.store_option) > 0: 
                res = sure(self, 'سوف يتم حذف جميع العمليات السابقة،\nهل تريد المواصلة؟')
                if res == -8:
                        self.store_option.clear()
                        self.store_option.append(['["new", "{}"]'.format(text,), 'ضع اسما جديدا هو "{}"'.format(text,)]) 
                        self.change_new_name()
            else:
                self.store_option.append(['["new", "{}"]'.format(text,), 'ضع اسما جديدا هو "{}"'.format(text,)]) 
                self.change_new_name()

    def add_of_now_name(self, option_ls, filename, a):
        # a = رقم الصف الذي يتم معالجته
        #option_ls = ["add", n, text, rev, pos, after, option]
        v = option_ls[5]
        if option_ls[1] == 0:
            if option_ls[4] == 0: new_name = option_ls[2]+filename
            elif option_ls[4] == 2: new_name = filename+option_ls[2]
            else: new_name = filename[:v]+option_ls[2]+filename[v:]
        #------------------------------------------------------     
        if option_ls[1] == 1:
            if a == 0: 
                try: self.first_n = int(option_ls[2])
                except: 
                    if option_ls[3] == 1: self.first_n = len(self.store_files)
                    else: self.first_n = 1
            if option_ls[6] == 1: 
                sn = str(self.first_n).replace('0','٠').replace('1','١').replace('2','٢').replace('3','٣').replace('4','٤').replace('5',
                                           '٥‌').replace('6','٦').replace('7','٧').replace('8','٨').replace('9','٩')
            else: sn = str(self.first_n)
            if option_ls[4] == 0: new_name = sn+filename
            elif option_ls[4] == 2: new_name = filename+sn
            else: new_name = filename[:v]+sn+filename[v:]
            if option_ls[3] == 1: self.first_n -= 1
            else: self.first_n += 1
        #------------------------------------------------------     
        if option_ls[1] == 5:
            if a == 0:
                self.n_s = None
                sr_n = option_ls[2].strip()
                for sr in SOWAR_ALQURAN:
                    if sr_n in sr:
                        self.n_s = SOWAR_ALQURAN.index(sr, )
                if self.n_s == None:
                    if option_ls[3] == 1: self.n_s = 113
                    else: self.n_s = 0
            if option_ls[6]== 0: sora_name = SOWAR_ALQURAN[self.n_s][1]
            else: sora_name = SOWAR_ALQURAN[self.n_s][0]
            if option_ls[4] == 0: new_name = sora_name+filename
            elif option_ls[4] == 2: new_name = filename+sora_name
            else: new_name = filename[:v]+sora_name+filename[v:]
            if option_ls[3] == 1: 
                self.n_s -= 1
            else: 
                self.n_s += 1
            if self.n_s not in range(-113, 114): self.n_s = 0
        #------------------------------------------------------     
        if option_ls[1] == 2:
            if a == 0:
                try: 
                    if option_ls[6]  == 0: n_la = LETTERS_HIDJAI.index(option_ls[2] .strip(), ) 
                    else: self.n_la = LETTERS_ABJADI.index(option_ls[2] .strip(), ) 
                except: 
                    if option_ls[3] == 1: self.n_la = 27
                    else: self.n_la = 0
            if option_ls[6]  == 0: letter = LETTERS_HIDJAI[self.n_la]
            else:  letter = LETTERS_ABJADI[self.n_la]
            if option_ls[4]  == 0: new_name = letter+filename
            elif option_ls[4]  == 2: new_name = filename+letter
            else: new_name = filename[:v]+letter+filename[v:]
            if option_ls[3] == 1: 
                self.n_la -= 1
            else: 
                self.n_la += 1
            if self.n_la not in range(-28, 28): self.n_la = 0
        #------------------------------------------------------     
        if option_ls[1] == 3:
            if a == 0:
                try: self.n_ll = LETTERS_LATIN.index(option_ls[2].strip(), ) 
                except: 
                    if option_ls[3] == 1: self.n_ll = 25
                    else: self.n_ll = 0
            if option_ls[6] == 1: letter = LETTERS_LATIN[self.n_ll].upper()
            else: letter = LETTERS_LATIN[self.n_ll]
            if option_ls[4] == 0: new_name = letter+filename
            elif option_ls[4] == 2: new_name = filename+letter
            else: new_name = filename[:v]+letter+filename[v:]
            if option_ls[3] == 1: 
                self.n_ll -= 1
            else: 
                self.n_ll += 1
            if self.n_ll not in range(-26, 26): self.n_ll = 0
        #------------------------------------------------------     
        if option_ls[1] == 4:
            if a == 0:
                try: self.no = int(option_ls[2])
                except: 
                    if option_ls[3] == 1: self.no = len(self.store_files)
                    else: self.no = 1
            if option_ls[6] == 1: 
                sno = self.get_ordinal(self.no, 1)
            else: sno = self.get_ordinal(self.no, 0)
            if option_ls[4] == 0: new_name = sno+filename
            elif option_ls[4] == 2: new_name = filename+sno
            else: new_name = filename[:v]+sno+filename[v:]
            if option_ls[3] == 1: self.no -= 1
            else: self.no+= 1
        return new_name

    
    def rp_in_now_name(self, option_ls, filename):
        # option_ls = ["rp", naw3, text_old or naw3, text_new, re_text]
        if option_ls[1] == 1:
            if option_ls[4] == 1: new_name = re.sub(option_ls[2], option_ls[3], filename)
            else:
                if option_ls[3] == 0: new_name = filename.replace(option_ls[2], option_ls[3])
                else: new_name = re.sub('['+option_ls[2]+']', option_ls[3], filename)
        else:
            if option_ls[2] == 0: new_name = re.sub('[أ-يءًٌٍَُِّْ]', option_ls[3], filename)
            elif option_ls[2] == 1: new_name = re.sub('[a-z]', option_ls[3], filename)
            elif option_ls[2] == 2: new_name = re.sub('[A-Z]', option_ls[3], filename)
            elif option_ls[2] == 3: new_name = re.sub('[a-zA-Z]', option_ls[3], filename)
            elif option_ls[2] == 4: new_name = re.sub('\d', option_ls[3], filename)
            elif option_ls[2] == 5: new_name = re.sub('[^\w\s]', option_ls[3], filename)
            elif option_ls[2] == 6: new_name = re.sub('\s', option_ls[3], filename)
            elif option_ls[2] == 7: new_name = re.sub('[^أ-يءًٌٍَُِّْ\s]', option_ls[3], filename)
            elif option_ls[2] == 8: new_name = re.sub('[^a-zA-Z\s]', option_ls[3], filename)
            elif option_ls[2] == 9: new_name = re.sub('[^\d]', option_ls[3], filename)
            elif option_ls[2] == 10: new_name = re.sub('[\w\s]', option_ls[3], filename)
            elif option_ls[2] == 11: new_name = re.sub('.*', option_ls[3], filename)
        return new_name
    
    def rm_from_now_name(self, option_ls, filename):
        # option_ls = ["rm", naw3, text or naw3, option, re_text]
        if option_ls[1] == 1:
            if option_ls[4] == 1: new_name = re.sub(option_ls[2], '', filename)
            else:
                if option_ls[3] == 0: new_name = filename.replace(option_ls[2], '')
                else: new_name = re.sub('['+option_ls[2]+']', '', filename)
        else:
            if option_ls[2] == 0: new_name = re.sub('[أ-يءًٌٍَُِّْ]', '', filename)
            elif option_ls[2] == 1: new_name = re.sub('[a-z]', '', filename)
            elif option_ls[2] == 2: new_name = re.sub('[A-Z]', '', filename)
            elif option_ls[2] == 3: new_name = re.sub('[a-zA-Z]', '', filename)
            elif option_ls[2] == 4: new_name = re.sub('\d', '', filename)
            elif option_ls[2] == 5: new_name = re.sub('[^\w\s]', '', filename)
            elif option_ls[2] == 6: new_name = re.sub('\s', '', filename)
            elif option_ls[2] == 7: new_name = re.sub('[^أ-يءًٌٍَُِّْ\s]', '', filename)
            elif option_ls[2] == 8: new_name = re.sub('[^a-zA-Z\s]', '', filename)
            elif option_ls[2] == 9: new_name = re.sub('[^\d]', '', filename)
            elif option_ls[2] == 10: new_name = re.sub('[\w\s]', '', filename)
            elif option_ls[2] == 11: new_name = re.sub('.*', '', filename)
        return new_name

    def change_new_name(self, *a):
        if len(self.store_option) == 0:
            for a in range(len(self.store_files)):
                iter0 = self.store_files.get_iter(a)
                self.store_files.set_value(iter0, 2, self.store_files.get_value(iter0, 1))
        for b in range(len(self.store_option)):
            iter1 = self.store_option.get_iter(b)
            option_ls = eval(self.store_option.get_value(iter1, 0))
            for a in range(len(self.store_files)):
                iter0 = self.store_files.get_iter(a)
                if b == 0:
                    filename, extension = self.split_ext(self.store_files.get_value(iter0, 3), self.store_files.get_value(iter0, 1))
                    new_name = filename
                else:
                    filename, extension = self.split_ext(self.store_files.get_value(iter0, 3), self.store_files.get_value(iter0, 2))
                    new_name = filename
                if option_ls[0] == 'new':
                    text = self.entry_new_name.get_text()
                    if text != '':
                        new_name = text
                elif option_ls[0] == 'add':
                    new_name = self.add_of_now_name(option_ls, new_name, a)
                elif option_ls[0] == 'rp':
                    new_name = self.rp_in_now_name(option_ls, new_name)
                elif option_ls[0] == 'rm':
                    new_name = self.rm_from_now_name(option_ls, new_name)
                self.store_files.set_value(iter0, 2, new_name+extension)
     
    def add_option_cb(self, *a):
            for a in self.hbox_add.get_children():
                self.hbox_add.remove(a)
            self.ch_add = obgect_1(self.add_option.get_active())
            self.hbox_add.pack_start(self.ch_add, True, True, 0)
            self.hbox_add.show_all()
                    
    def add_btn_cb(self, *a):
        name = self.add_option.get_active_text()
        n = self.add_option.get_active()
        text = self.ch_add.entry_start.get_text()
        pos = self.ch_add.pos_object.get_active()
        after = self.ch_add.pos_after.get_value()
        option = self.ch_add.option_object.get_active()
        rev = self.ch_add.reverse.get_active()
        text0 = ''
        if n == 0: text0 = ' هو "{}"'.format(text,)
        elif text != '': text0 = ' أوّلها "{}"'.format(text,)
        if rev == True: rev0 = ' مرتبة عكسيّا'
        else: rev0 = ''
        if n == 0: option0 = ''
        else: option0 = ' '+self.ch_add.option_object.get_active_text()
        pos0 = ' '+self.ch_add.pos_object.get_active_text()
        if pos != 1: pos00 = ''
        else: pos00 = ' بعد الحرف {} '.format(int(after),)
        self.store_option.append(['["add", {}, "{}", {}, {}, {}, {}]'.format(n, text, rev, pos, after, option), 
                                  'أضف{} {}{}{}{}{}'.format(pos0, pos00, name, option0, rev0, text0)]) 
        self.change_new_name()
    
    def rm_btn_cb(self, btn, v):
        ls1 = []# ls1 = ["rm", naw3, text or naw3, option, re_text]
        ls1.append("rm")
        if v == 0:
            ls1.append(1)
            text = 'حذف : "'+self.entry_del_text.get_text()+'"'
            if self.re_del_text.get_active(): text += ' ، تعبير قياسي'
            else: text += ' ، '+self.del_text_option.get_active_text()
            ls1.append(self.entry_del_text.get_text())
            ls1.append(self.del_text_option.get_active())
            ls1.append(self.re_del_text.get_active())
        else:
            ls1.append(2)
            text = 'حذف : "'+self.del_naw3_option.get_active_text()+'"'
            ls1.append(self.del_naw3_option.get_active())
        text1 = repr(ls1)
        self.store_option.append([text1, text]) 
        self.change_new_name()
    
    def rp_btn_cb(self, btn, v):
        ls1 = []# ls1 = [replace=3, naw3, text_old or naw3, text_new, re_text]
        ls1.append("rp")
        if v == 0:
            ls1.append(1)
            text = 'استبدال : "'+self.entry_replace_text_old.get_text()+'" بالنص : "'+self.entry_replace_text_new.get_text()+'"'
            ls1.append(self.entry_replace_text_old.get_text())
            ls1.append(self.entry_replace_text_new.get_text())
            if self.re_replace_text.get_active(): 
                text += ' ، تعبير قياسي'
                ls1.append(1)
            else:  ls1.append(0)
        else:
            ls1.append(2)
            text = 'استبدال : "'+self.replace_naw3_option.get_active_text()+'" بالنص : "'+self.entry_replace_naw3_new.get_text()+'"'
            ls1.append(self.replace_naw3_option.get_active())
            ls1.append(self.entry_replace_naw3_new.get_text())
        text1 = repr(ls1)
        self.store_option.append([text1, text]) 
        self.change_new_name()
    
    def get_ordinal(self, n, i):
        a3 = int(n/100)
        a2 = int((n%100)/10)
        a1 = int(n%10)
        name = '{} و{} بعد {}'.format(NAME_ORDINAL_ONE[a1],NAME_ORDINAL_TEN[a2],NAME_ORDINAL_hundred[a3])
        name = name.replace(' وo', '')
        name = name.replace(' بعد o', '')
        name = name.replace('o وعشر', 'العاشر')
        name = name.replace('o و', '')
        name = name.replace('o بعد', '')
        name = name.replace('وعشر', 'عشر')
        if a2 == 0: name = name.replace('الحادي', 'الأول')
        if i == 1:
            name = name.replace(r'عشر', r'عشرة')
            name = name.replace(r'العاشر', r'العاشرة')
            name = name.replace(r'الحادي', r'الحادية')
            name = name.replace(r'الثاني', r'الثانية')
            name = name.replace(r'الثالث', r'الثالثة')
            name = name.replace(r'الرابع', r'الرابعة')
            name = name.replace(r'الخامس', r'الخامسة')
            name = name.replace(r'السادس', r'السادسة')
            name = name.replace(r'السابع', r'السابعة')
            name = name.replace(r'الثامن', r'الثامنة')
            name = name.replace(r'التاسع', r'التاسعة')
            name = name.replace(r'الأول', r'الأولى')
            name = name.replace(r'عشرةو', r'عشرو')
        return name 
    
    def build(self, *a):
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        hb_bar.set_title('المسمّي')
        hb_bar.set_subtitle('إعادة تسمية مجموعة من الملفات')
        
        self.set_default_size(1000, 700)
        self.set_border_width(3)
        
        #----------------------------------------------------------------------------------
        vbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btnbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(btnbox.get_style_context(), "linked")
        
        menu_add = Gtk.Menu()   
        add_files = Gtk.MenuItem("أضف ملفات")
        add_files.connect('activate', self.add_files_cb)
        menu_add.append(add_files)     
        add_folder = Gtk.MenuItem("أضف مجلدات")
        add_folder.connect('activate', self.add_folders_cb)
        menu_add.append(add_folder)
        btn_add = Gtk.MenuButton()
        btn_add.set_popup (menu_add)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_NEW, Gtk.IconSize.BUTTON)
        btn_add.set_image(img)
        menu_add.show_all();
        btnbox.pack_start(btn_add, False, False, 0)
        
        go_up = Gtk.Button()
        go_up.set_tooltip_text("ارفع الملف المحدد")
        go_up.connect('clicked', lambda *a: self.move_file(-1))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_UP, Gtk.IconSize.BUTTON)
        go_up.set_image(img)
        btnbox.pack_start(go_up, False, False, 0)
        
        go_down = Gtk.Button()
        go_down.set_tooltip_text("أنزل الملف المحدد")
        go_down.connect('clicked', lambda *a: self.move_file(1))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.BUTTON)
        go_down.set_image(img)
        btnbox.pack_start(go_down, False, False, 0)
        
        remove = Gtk.Button()
        remove.set_tooltip_text("حذف الملف المحدد")
        remove.connect('clicked', self.remove_file)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.BUTTON)
        remove.set_image(img)
        btnbox.pack_start(remove, False, False, 0)
        
        remove_all = Gtk.Button()
        remove_all.set_tooltip_text("حذف جميع الملفات")
        remove_all.connect('clicked', self.remove_files)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.BUTTON)
        remove_all.set_image(img)
        btnbox.pack_start(remove_all, False, False, 0)
        
        rename_btn = Gtk.Button('أعد التسمية')
        rename_btn.set_tooltip_text("أعد تسمية الملفات")
        rename_btn.connect('clicked', self.start_rename)
        hb_bar.pack_start(rename_btn)
        about = Gtk.Button()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_ABOUT, Gtk.IconSize.BUTTON)
        about.set_image(img)
        about.connect('clicked', lambda *a: About(self))
        hb_bar.pack_start(about)
        vbox.pack_start(btnbox, False, False, 0)
        
        #------------------------------------------------------------------------------------
        self.store_files = Gtk.ListStore(GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, 
                                          GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.tree_files = Gtk.TreeView(self.store_files)
        self.sel_files = self.tree_files.get_selection()
        self.tree_files.set_rules_hint(True)
        self.tree_files.set_grid_lines(3)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("#", celltoggle)
        columntoggle.add_attribute( celltoggle, "active", 0)
        celltoggle.connect('toggled', self.fixed_toggled_field, self.store_files)
        self.tree_files.append_column(columntoggle)
        columntext_now= Gtk.TreeViewColumn("الاسم الحالي", celltext, text = 1 )
        self.tree_files.append_column(columntext_now)
        columntext_new = Gtk.TreeViewColumn("الاسم الجديد", celltext, text = 2 )
        columntext_new.set_expand(True)
        self.tree_files.append_column(columntext_new)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_files)
        vbox.pack_start(scroll,True, True, 0)
        self.tree_files.columns_autosize()

        #----------------------------------------------------------------------------------
        hbox1 = Gtk.Box(spacing=1,orientation=Gtk.Orientation.HORIZONTAL)
        btnbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        go_up2 = Gtk.Button()
        go_up2.set_tooltip_text("ارفع العملية المحدد")
        go_up2.connect('clicked', lambda *a: self.move_option(-1))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_UP, Gtk.IconSize.BUTTON)
        go_up2.set_image(img)
        btnbox2.pack_start(go_up2, False, False, 0)
        
        go_down2 = Gtk.Button()
        go_down2.set_tooltip_text("أنزل العملية المحدد")
        go_down2.connect('clicked', lambda *a: self.move_option(1))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.BUTTON)
        go_down2.set_image(img)
        btnbox2.pack_start(go_down2, False, False, 0)
        
        remove2 = Gtk.Button()
        remove2.set_tooltip_text("حذف العملية المحددة")
        remove2.connect('clicked', self.remove_option)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.BUTTON)
        remove2.set_image(img)
        btnbox2.pack_start(remove2, False, False, 0)
        remove_all2 = Gtk.Button()
        remove_all2.set_tooltip_text("حذف جميع العمليات")
        remove_all2.connect('clicked', self.remove_options)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.BUTTON)
        remove_all2.set_image(img)
        btnbox2.pack_start(remove_all2, False, False, 0)
        
        #-------------------------------------------------------------------------------------------
        self.store_option = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.tree_option = Gtk.TreeView(self.store_option)
        self.sel_option = self.tree_option.get_selection()
        self.tree_option.set_rules_hint(True)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        columntext= Gtk.TreeViewColumn("العمليات", celltext, text = 1 )
        self.tree_option.append_column(columntext)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_option)
        hbox1.pack_start(scroll, True, True, 0)
        hbox1.pack_start(btnbox2, False, False, 0)
        vbox.pack_start(hbox1, False, False, 0)
        
        #------------------------------------------------------------------------------------
        notebk = Gtk.Notebook()
        notebk.set_tab_pos(Gtk.PositionType.LEFT)
        
        #------------------------------------------------------------------------------------
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(7)
        add_new_name = Gtk.Button('ضع اسمًا جديدًا')
        add_new_name.connect('clicked', self.add_new_name_cb)
        grid.attach(add_new_name, 0, 0, 2, 1)
        self.entry_new_name = Gtk.Entry()
        self.entry_new_name.set_placeholder_text('ضع اسمًا جديدًا')
        grid.attach(self.entry_new_name, 2, 0, 6, 1)
        notebk.append_page(grid, Gtk.Label('جديد'))

        #------------------------------------------------------------------------------------
        grid = Gtk.Grid()
        self.hbox_add = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(7)
        add_btn= Gtk.Button('أضف')
        add_btn.connect('clicked', self.add_btn_cb)
        grid.attach(add_btn, 0, 0, 2, 1)
        self.add_option= Gtk.ComboBoxText()
        for a in ['نصًّا','أرقامًا','حروفًا عربيّةً','أحرفًا لاتينيّةً','أعدادًا ترتيبيّةً','أسماء سورٍ']:
            self.add_option.append_text(a)
        self.add_option.connect('changed', self.add_option_cb)
        self.add_option.set_active(0)
        grid.attach(self.add_option, 2, 0, 6, 1)
        grid.attach(self.hbox_add, 0, 1, 8, 1)
        notebk.append_page(grid, Gtk.Label('إضافة'))
        
        #------------------------------------------------------------------------------------
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(7)
        self.replace_text = Gtk.Button('استبدال')
        self.replace_text.connect('clicked', self.rp_btn_cb, 0)
        self.entry_replace_text_old = Gtk.Entry()
        self.entry_replace_text_new = Gtk.Entry()
        self.re_replace_text = Gtk.CheckButton('تعبير قياسي')
        grid.attach(self.replace_text, 0, 0, 1, 1)
        grid.attach(self.entry_replace_text_old, 1, 0, 3, 1)
        grid.attach(self.entry_replace_text_new, 4, 0, 3, 1)
        grid.attach(self.re_replace_text, 7, 0, 1, 1)
        self.replace_naw3 = Gtk.Button('استبدال')
        self.replace_naw3.connect('clicked', self.rp_btn_cb, 1)
        self.replace_naw3_option= Gtk.ComboBoxText()
        for a in ['الحروف العربية', 'الحروف اللاتينة الصغيرة', 'الحروف اللاتينة الكبيرة', 'كل الحروف اللاتينة', 'الأرقام', 'الرموز', 'المسافات'
                  ,'كل شيء ما عدا الحروف العربية', 'كل شيء ما عدا الحروف اللاتينة', 'كل شيء ما عدا الأرقام', 'كل شيء ما عدا الرموز', 'كل شيء']:
            self.replace_naw3_option.append_text(a)
        self.replace_naw3_option.set_active(0)
        self.entry_replace_naw3_new = Gtk.Entry()
        grid.attach(self.replace_naw3, 0, 1, 1, 1)
        grid.attach(self.replace_naw3_option, 1, 1, 3, 1)
        grid.attach(self.entry_replace_naw3_new, 4, 1, 3, 1)
        notebk.append_page(grid, Gtk.Label('استبدال'))
        
        #------------------------------------------------------------------------------------
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(7)
        self.del_text = Gtk.Button('حذف')
        self.del_text.connect('clicked', self.rm_btn_cb, 0)
        self.entry_del_text = Gtk.Entry()
        self.del_text_option= Gtk.ComboBoxText()
        for a in ['نص عادي', 'حروف متفرقة']:
            self.del_text_option.append_text(a)
        self.del_text_option.set_active(0)
        self.re_del_text = Gtk.CheckButton('تعبير قياسي')
        grid.attach(self.del_text, 0, 0, 1, 1)
        grid.attach(self.entry_del_text, 1, 0, 4, 1)
        grid.attach(self.del_text_option, 5, 0, 1, 1)
        grid.attach(self.re_del_text, 6, 0, 1, 1)
        self.del_naw3 = Gtk.Button('حذف')
        self.del_naw3.connect('clicked', self.rm_btn_cb, 1)
        self.del_naw3_option= Gtk.ComboBoxText()
        for a in ['الحروف العربية', 'الحروف اللاتينة الصغيرة', 'الحروف اللاتينة الكبيرة', 'كل الحروف اللاتينة', 'الأرقام', 'الرموز', 'المسافات'
                  ,'كل شيء ما عدا الحروف العربية', 'كل شيء ما عدا الحروف اللاتينة', 'كل شيء ما عدا الأرقام', 'كل شيء ما عدا الرموز', 'كل شيء']:
            self.del_naw3_option.append_text(a)
        self.del_naw3_option.set_active(0)
        grid.attach(self.del_naw3, 0, 1, 1, 1)
        grid.attach(self.del_naw3_option, 1, 1, 2, 1)
        notebk.append_page(grid, Gtk.Label('حذف'))
        vbox.pack_start(notebk, False, False, 0)
        
        #------------------------------------------------------------------------------------
        self.add(vbox)
        self.show_all()
        

class obgect_1(Gtk.Grid):
    
    def pos_object_cb(self, btn):
        if btn.get_active() == 1:
            self.pos_after.set_sensitive(True)
        else:
            self.pos_after.set_sensitive(False)
    
    def __init__(self, n):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(7)
        self.entry_start = Gtk.Entry()
        self.entry_start.set_placeholder_text(list_anw3[n][0])
        self.option_object= Gtk.ComboBoxText()
        for a in list_anw3[n][1]:
            self.option_object.append_text(a)
        self.option_object.set_active(0)
        self.pos_object= Gtk.ComboBoxText()
        for a in ['في الأول', 'في الوسط', 'في الأخير']:
            self.pos_object.append_text(a)
        self.pos_object.set_active(0)
        self.pos_object.connect('changed', self.pos_object_cb)
        adj = Gtk.Adjustment(1, 1, 100, 1, 5, 0)
        self.pos_after = Gtk.SpinButton()
        self.pos_after.set_adjustment(adj)
        self.pos_after.set_value(1.0)
        self.pos_after.set_sensitive(False)
        self.reverse = Gtk.CheckButton('عكسي   ')    
        self.attach(self.entry_start, 0, 1, 2, 1)
        self.attach(self.pos_object, 3, 1, 1, 1)
        self.attach(Gtk.Label('بعد الحرف :'), 4, 1, 1, 1)
        self.attach(self.pos_after, 5, 1, 1, 1)
        if n != 0:
            self.attach(self.option_object, 6, 1, 1, 1)
            self.attach(self.reverse, 2, 1, 1, 1)

class About(Gtk.AboutDialog):
    
    def __init__(self, parent):
        self.parent = parent
        Gtk.AboutDialog.__init__(self, parent = self.parent, wrap_license = True)
        self.set_program_name("المسمّي")
        self.set_version("0.2.2")
        #self.set_logo_icon_name('logo')
        self.set_comments("""برنامج إعادة تسمية مجموعة ملفات معا""")
        self.set_authors(['',
                          '<asmaaarab@gmail.com> أحمد رغدي ',
                           ])
        self.set_license("""
        رخصة وقف العامة
        http://www.ojuba.org/wiki/doku.php/waqf/license
        """)
        self.run()
        self.destroy()

RenameAll()   
def main(): 
    Gtk.main()

if __name__ == "__main__":
    main()
