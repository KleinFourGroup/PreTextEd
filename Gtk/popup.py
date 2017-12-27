#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

tips = {"printf": "(const char *format, ...)",
        "fprintf": "(FILE *stream, const char *format, ...)",
        "sprintf": "(char *str, const char *format, ...)",
        "snprintf": "(char *str, size_t size, const char *format, ...)",
        "fputc": "(int c, FILE *stream)",
        "fputs": "(const char *s, FILE *stream)",
        "putc": "(int c, FILE *stream)",
        "putchar": "(int c)",
        "puts": "(const char *s)"}

tip_win = None

def get_tip(text):
    for fn in tips.keys():
        if text == fn:
            return tips[fn]
    return None
def tip_window_new(tip):
    """
  GdkColormap *cmap;
  GdkColor color;
  PangoFontDescription *pfd;
    """
    win = Gtk.Window(Gtk.WindowType.POPUP)
    # gtk_container_set_border_width (GTK_CONTAINER (win), 0);
    eb = Gtk.EventBox()
    #  gtk_container_set_border_width (GTK_CONTAINER (eb), 1);
    win.add(eb)
    label = Gtk.Label(tip)
    eb.add(label)
    """
  pfd = pango_font_description_from_string ("courier");
  gtk_widget_modify_font (label, pfd);
  
  cmap = gtk_widget_get_colormap (win);
  color.red = 0;
  color.green = 0;
  color.blue = 0;
  if (gdk_colormap_alloc_color (cmap, &color, FALSE, TRUE))
    gtk_widget_modify_bg (win, GTK_STATE_NORMAL, &color);
  else
    g_warning ("Color allocation failed!\n");

  cmap = gtk_widget_get_colormap (eb);
  color.red = 65535;
  color.green = 65535;
  color.blue = 45535;
  if (gdk_colormap_alloc_color (cmap, &color, FALSE, TRUE))
    gtk_widget_modify_bg (eb, GTK_STATE_NORMAL, &color);
  else
    g_warning ("Color allocation failed!\n");
    """
    return win

def insert_open_brace(text_view, loc):
    global tip_win

    # Get the word at cursor.
    start = loc.copy()
    if not start.backward_word_start():
        return
    text = start.get_text(loc)
    text = text.strip();
    
    # Get the corresponding tooltip.
    tip_text = get_tip(text);  
    if tip_text == None:
        return
  
    # Calculate the tool tip window location.
    buf_loc = text_view.get_iter_location(loc)
    print("Buffer: %d, %d\n" % (buf_loc.x, buf_loc.y))
    win_x, win_y = text_view.buffer_to_window_coords(Gtk.TextWindowType.WIDGET, buf_loc.x, buf_loc.y)
    print("Window: %d, %d\n" % (win_x, win_y))
    win = text_view.get_window(Gtk.TextWindowType.WIDGET)
    dummy, x, y = win.get_origin()

    # Destroy any previous tool tip window.
    if tip_win:
        tip_win.destroy()
  
    # Create a new tool tip window and place it at the caculated location.
    tip_win = tip_window_new (tip_text)
    tip_win.move (win_x + x, win_y + y + buf_loc.height)
    tip_win.show_all()

def insert_close_brace():
    global tip_win
    if tip_win:
        tip_win.destroy()
        tip_win = None

def buffer_insert_text(buf, loc, text, l, text_view):
    if text == "(":
        insert_open_brace(text_view, loc)
    elif text == ")":
        insert_close_brace()

def main():
    # gtk_init (&argc, &argv);

    # Create the window.
    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)

    # Create the text widget inside a scrolled window.
    swindow = Gtk.ScrolledWindow()
    swindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    win.add(swindow)

    text_view = Gtk.TextView()
    buf = text_view.get_buffer()
    buf.connect("insert-text", buffer_insert_text, text_view)
    swindow.add(text_view)

    # pfd = pango_font_description_from_string ("courier");
    # gtk_widget_modify_font (text_view, pfd);
  
    win.show_all()

    Gtk.main()

main()
