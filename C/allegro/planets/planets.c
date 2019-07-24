//By Juan Tec

#include <stdio.h>
#include <allegro5/allegro.h>
#include <allegro5/allegro_image.h>
#include <allegro5/allegro_native_dialog.h>
 
int menu = 0;

const float FPS = 60;
const int SCREEN_W = 640;
const int SCREEN_H = 480;
enum MYKEYS
{
   KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER
};

int main(int argc, char **argv)
{  
   int x = 200;
   bool key[4] = { false, false, false, false };
   bool redraw = true;
   bool doexit = false;

   if(!al_init()) {
      fprintf(stderr, "failed to initialize allegro!\n");
      return -1;
   }

   ALLEGRO_DISPLAY* display = al_create_display(SCREEN_W, SCREEN_H);
   if(!display) {
      fprintf(stderr, "failed to create display!\n");
      return -1;
   }

   ALLEGRO_TIMER* timer = al_create_timer(1.0 / FPS);
   if(!timer) {
      fprintf(stderr, "failed to create timer!\n");
      al_destroy_display(display);
      return -1;
   }

   if(!al_init_image_addon()) {
      al_show_native_message_box(display, "Error", "Error", "Failed to initialize al_init_image_addon!", 
                                 NULL, ALLEGRO_MESSAGEBOX_ERROR);
      return -1;
   }
 
   if(!al_install_keyboard()) {
      fprintf(stderr, "failed to initialize the keyboard!\n");
      return -1;
   }

   ALLEGRO_BITMAP* image = al_load_bitmap("pictures/1.png");
	if(!image)
	{
      al_show_native_message_box(display, "Error", "Error", "Failed to load image 1!", 
                                 NULL, ALLEGRO_MESSAGEBOX_ERROR);
      al_destroy_display(display);
      return -1;
   }

   ALLEGRO_BITMAP* image2 = al_load_bitmap("pictures/2.png");
	if(!image2)
	{
      al_show_native_message_box(display, "Error", "Error", "Failed to load image 2!", 
                                 NULL, ALLEGRO_MESSAGEBOX_ERROR);
      al_destroy_display(display);
      return -1;
   }

   ALLEGRO_BITMAP* sel = al_load_bitmap("pictures/sel.png");
	if(!sel)
	{
      al_show_native_message_box(display, "Error", "Error", "Failed to load image 3!", 
                                 NULL, ALLEGRO_MESSAGEBOX_ERROR);
      al_destroy_display(display);
      return -1;
   }

   ALLEGRO_BITMAP* bg = al_load_bitmap("pictures/bg.jpg");
	if(!bg)
	{
      al_show_native_message_box(display, "Error", "Error", "Failed to load background!", 
                                 NULL, ALLEGRO_MESSAGEBOX_ERROR);
      al_destroy_display(display);
      return -1;
   }
 
   ALLEGRO_EVENT_QUEUE* event_queue = al_create_event_queue();
   if(!event_queue) {
      fprintf(stderr, "failed to create event_queue!\n");
      al_destroy_bitmap(sel);
      al_destroy_display(display);
      al_destroy_timer(timer);
      return -1;
   }

   al_register_event_source(event_queue, al_get_display_event_source(display));
   al_register_event_source(event_queue, al_get_timer_event_source(timer));
   al_register_event_source(event_queue, al_get_keyboard_event_source());

   al_clear_to_color(al_map_rgb(0,0,0));

   al_draw_bitmap(bg, 0, 0, 0);
   al_draw_scaled_bitmap(image, 0, 0, al_get_bitmap_width(image), al_get_bitmap_height(image), 200, 200, 100, 100, 0);
   al_draw_scaled_bitmap(image2, 0, 0, al_get_bitmap_width(image2), al_get_bitmap_height(image2), 350, 200, 100, 100, 0);
   al_draw_bitmap(sel, x, 200, 0);
 
   al_flip_display();
 
   al_start_timer(timer);
 
   while(!doexit)
   {
      ALLEGRO_EVENT ev;
      al_wait_for_event(event_queue, &ev);
 
      if(ev.type == ALLEGRO_EVENT_TIMER)
      {
         if(key[KEY_LEFT] && x >= 350)
         {
            x -= 150;
            redraw = true;  
         }
         if(key[KEY_RIGHT] && x <= 200)
         {
            x += 150;
            redraw = true;
         }
         if(key[KEY_ENTER])
         {
            key[KEY_ENTER] = false;
            switch(menu)
            {
               case 0:
                  menu = 1;
                  break;
               case 1:
                  menu = 0;
                  break;
            }
            redraw = true;
         }
      }
      else if(ev.type == ALLEGRO_EVENT_DISPLAY_CLOSE) {
         break;
      }
      else if(ev.type == ALLEGRO_EVENT_KEY_DOWN)
      {
         switch(ev.keyboard.keycode)
         {
            case ALLEGRO_KEY_LEFT: 
               key[KEY_LEFT] = true;
               break;
            case ALLEGRO_KEY_RIGHT:
               key[KEY_RIGHT] = true;
               break;
            case ALLEGRO_KEY_ENTER:
               key[KEY_ENTER] = true;
               break;
         }
      }
      else if(ev.type == ALLEGRO_EVENT_KEY_UP)
      {
         switch(ev.keyboard.keycode)
         {
            case ALLEGRO_KEY_LEFT: 
               key[KEY_LEFT] = false;
               break;
            case ALLEGRO_KEY_RIGHT:
               key[KEY_RIGHT] = false;
               break;
            // case ALLEGRO_KEY_ENTER:
            //    key[KEY_ENTER] = false;
            //    break;
            case ALLEGRO_KEY_ESCAPE:
               //Pending go back action
               break;
         }
      }
 
   if(redraw && al_is_event_queue_empty(event_queue))
	{
      redraw = false;
      al_clear_to_color(al_map_rgb(0,0,0));
		al_draw_bitmap(bg, 0, 0, 0);
		
      switch(menu)
      {
      case 0:
         al_draw_scaled_bitmap(image, 0, 0, al_get_bitmap_width(image), al_get_bitmap_height(image), 200, 200, 100, 100, 0);
         al_draw_scaled_bitmap(image2, 0, 0, al_get_bitmap_width(image2), al_get_bitmap_height(image2), 350, 200, 100, 100, 0);
         al_draw_bitmap(sel, x, 200, 0);
         break;
      case 1:
         //draw planet menu
         break;
      }
      al_flip_display();
      }
   }
 
   al_destroy_bitmap(bg);
   al_destroy_bitmap(sel);
   al_destroy_bitmap(image);
   al_destroy_bitmap(image2);
   al_destroy_timer(timer);
   al_destroy_display(display);
   al_destroy_event_queue(event_queue);
 
   return 0;
}