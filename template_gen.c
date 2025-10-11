#include <stdio.h> 
#include <stdlib.h>
#include <cairo.h> 

typedef struct {
    int width;
    int height;
    cairo_surface_t *surface;
    // current state of drawing, drawing always done to cairo_t
    cairo_t *cr; 
} Template;

// struct to hold the rgb color value
typedef struct {
    double r, g, b;
} Color;

// converts hex color string to rgb values to use
Color hex_to_rgb(const char *hx) {
    Color color;
    unsigned int value;
    if (hx[0] == '#') {
        hx = hx + 1;
    }
    sscanf(hx, "%x", &value);
    color.r = ((value >> 16) & 0xFF) / 255.0;
    color.g = ((value >> 8) & 0xFF) / 255.0;
    color.b = (value & 0xFF) / 255.0;
    return color;
}


// create the image template by allocating memory for struct
// and setting values, then creating the surface and context
Template* create_temp(int width, int height) {
    Template *tg = malloc(sizeof(Template));
    // access struct members w pointer
    tg->width = width;
    tg->height = height;
    tg->surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, width, height);

    // create the drawing context
    tg->cr = cairo_create(tg->surface);
    return tg;
}

// this sets the bakcground color of the template
void temp_set_bg(Template *tg, const char *hxcolor) {
    Color color = hex_to_rgb(hxcolor);
    // set the background color
    cairo_set_source_rgb(tg->cr, color.r, color.g, color.b);
    // fill the surface with the color
    cairo_paint(tg->cr);
}

// add a gradient background
void temp_set_gradient(Template *tg, const char *c1, const char *c2,
int ver) {
    Color one = hex_to_rgb(c1);
    Color two = hex_to_rgb(c2);
    cairo_pattern_t *pat;
    if (ver) {
        pat = cairo_pattern_create_linear(0, 0, 0, tg->height);
    } 
    else {
        pat = cairo_pattern_create_linear(0, 0, tg->width, 0);
    }

    cairo_pattern_add_color_stop_rgb(pat, 0, one.r, one.g, one.b);
    cairo_pattern_add_color_stop_rgb(pat, 1, two.r, two.g, two.b);
    cairo_set_source(tg->cr, pat);
    cairo_paint(tg->cr);
    cairo_pattern_destroy(pat);
}


// this adds the text to the template by initializing the font,
// size, color, and position
void temp_add_text(Template *tg, char *text, int x, int y) {
    // font creation
    cairo_select_font_face(tg->cr, "Sans", CAIRO_FONT_SLANT_NORMAL,
    CAIRO_FONT_WEIGHT_BOLD);

    // font size
    cairo_set_font_size(tg->cr, 40.0);

    // font color which is gonna be white
    cairo_set_source_rgb(tg->cr, 1.0, 1.0, 1.0);

    // draw the text at x,y position
    cairo_move_to(tg->cr, x, y);
    cairo_show_text(tg->cr, text);

}

// Add image/logo from PNG file
void temp_add_logo(Template *tg, const char *image_path, int x, int y, int width, int height) {
    cairo_surface_t *image = cairo_image_surface_create_from_png(image_path);
    
    if (cairo_surface_status(image) != CAIRO_STATUS_SUCCESS) {
        printf("Error loading image: %s\n", image_path);
        cairo_surface_destroy(image);
        return;
    }
    
    // Get original dimensions
    int img_width = cairo_image_surface_get_width(image);
    int img_height = cairo_image_surface_get_height(image);
    
    // Calculate scale
    double scale_x = (double)width / img_width;
    double scale_y = (double)height / img_height;
    
    // Save context state
    cairo_save(tg->cr);
    
    // Move to position and scale
    cairo_translate(tg->cr, x, y);
    cairo_scale(tg->cr, scale_x, scale_y);
    
    // Draw image
    cairo_set_source_surface(tg->cr, image, 0, 0);
    cairo_paint(tg->cr);
    
    // Restore context
    cairo_restore(tg->cr);
    
    cairo_surface_destroy(image);
}

// add rectangle for borders or backgrounds
void temp_add_rectangle(Template *tg, int x, int y, int width, int height, 
                       const char *fill_color, const char *outline_color, int outline_width) {
    if (fill_color != NULL) {
        Color fill = hex_to_rgb(fill_color);
        cairo_set_source_rgb(tg->cr, fill.r, fill.g, fill.b);
        cairo_rectangle(tg->cr, x, y, width, height);
        cairo_fill(tg->cr);
    }
    
    if (outline_color != NULL) {
        Color outline = hex_to_rgb(outline_color);
        cairo_set_source_rgb(tg->cr, outline.r, outline.g, outline.b);
        cairo_set_line_width(tg->cr, outline_width);
        cairo_rectangle(tg->cr, x, y, width, height);
        cairo_stroke(tg->cr);
    }
}


// this saves the template to a png file before freeing the mem
void save_temp(Template *tg, char *filename) {
    // write the surface to a png file
    cairo_surface_write_to_png(tg->surface, filename);
    // print the confirmation message
    printf("Saved image to %s\n", filename);
}

// cleanup and free the allocated memory by destroying the 
// cairo context and surface and then freeing the struct
void free_temp(Template *tg) {
    cairo_destroy(tg->cr);
    cairo_surface_destroy(tg->surface);
    free(tg);
}

// this calls the python script to generate the ai enhanced image
int generate_aibg(const char *theme, const char *output_path) {
    char command[512];
    snprintf(command, sizeof(command), "python3 ai_enhance.py '%s' '%s'",
             theme, output_path);
    printf("Generating AI background...\n");
    int result = system(command);

    return (result == 0);
}

int main() {
    printf("Generating template...\n");

    // generate the ai background first
    generate_aibg("Blockchain Research Event", "output/bg_temp.png");

    // create the template
    Template *tg = create_temp(1024, 1024);

    // load the ai generated background
    temp_add_logo(tg, "output/bg_temp.png", 0, 0, 1024, 1024);

    // add a slightly transparent overlay to darken bg
    cairo_set_source_rgba(tg->cr, 0, 0, 0, 0.4);
    cairo_paint(tg->cr);

    // add logo
    temp_add_logo(tg, "Logo Design.png", 80, 60, 180, 180);

    // add text
    temp_add_text(tg, "Northeastern Blockchain", 290, 150);

    // add title
    cairo_set_font_size(tg->cr, 70);
    temp_add_text(tg, "Research Event", 80, 450);

    // save the template to a file
    save_temp(tg, "output_template.png");

    // free the memory and destroy the template
    free_temp(tg);

    // done w creation
    printf("Template generation is complete!\n");
    return 0;
}