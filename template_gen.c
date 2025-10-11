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


int main() {
    printf("Generating template...\n");

    // create the template
    Template *tg = create_temp(800, 600);

    // set the background to black
    cairo_set_source_rgb(tg->cr, 0, 0, 0);
    cairo_paint(tg->cr);

    // add text
    temp_add_text(tg, "Hello, World!", 200, 300);

    // save the template to a file
    save_temp(tg, "first_template.png");

    // free the memory and destroy the template
    free_temp(tg);

    // done w creation
    printf("Template generation is complete!\n");
    return 0;
}