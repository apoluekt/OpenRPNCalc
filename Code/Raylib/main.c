#include "raylib.h"
#include <stdint.h>

#include <emscripten/emscripten.h>

#include "calc.h"
#include "sharp.h"

#define SCREEN_WIDTH 490
#define SCREEN_HEIGHT 901

int keymap[49] = {
  0,  // 0
  KEY_ZERO, // 1 
  KEY_GRAVE,  // 2
  KEY_PERIOD,  // 3
  KEY_U, // 4
  KEY_ENTER, // 5
  0, // 6
  KEY_ONE, // 7
  KEY_TWO, // 8
  KEY_THREE, // 9 
  KEY_EQUAL, // 10
  KEY_MINUS, // 11
  0, // 12 
  KEY_FOUR, // 13
  KEY_FIVE, // 14
  KEY_SIX, // 15
  KEY_BACKSLASH, // 16
  KEY_SLASH, // 17
  0, // 18 
  KEY_SEVEN, // 19
  KEY_EIGHT, // 20
  KEY_NINE, // 21
  KEY_X, // 22 
  KEY_BACKSPACE, // 23
  0, // 24
  KEY_Q, // 25 
  KEY_I, // 26
  KEY_R, // 27
  KEY_P, // 28
  KEY_G, // 29
  KEY_Z, // 30 
  KEY_W, // 31
  KEY_N, // 32
  KEY_D, // 33
  KEY_S, // 34
  KEY_C, // 35
  KEY_T, // 36
  KEY_SPACE, // 37 
  KEY_TAB, // 38
  KEY_SEMICOLON, // 39
  KEY_M, // 40
  KEY_LEFT_BRACKET, // 41
  KEY_RIGHT_BRACKET, // 42
  KEY_LEFT_SHIFT, // 43
  KEY_LEFT_CONTROL, // 44
  KEY_F5, // 45
  KEY_F6, // 46
  KEY_F7, // 47
  KEY_F8, // 48
};

Texture2D texture; 
int block; 

int keycode_from_xy(int x, int y) {
  int large_y[4] = {
    814, 750, 681, 616
  }; 
  int large_x[5] = {
    42, 124, 207, 290, 371
  }; 
  int small_y[4] = {
    553, 491, 429, 368
  }; 
  int small_x[6] = {
    43, 110, 179, 246, 316, 385
  }; 
  for (int i=0; i<4; i++) {
    if (y>=large_y[i] && y<= large_y[i] + 44) {
      for (int j=0; j<5; j++) {
        if (x>=large_x[j] && x<=large_x[j] + 73) {
          return i*6 + j + 1; 
        }
      }
    }
  }
  for (int i=0; i<4; i++) {
    if (y>=small_y[i] && y<= small_y[i] + 39) {
      for (int j=0; j<6; j++) {
        if (x>=small_x[j] && x<=small_x[j] + 62) {
          return i*6 + j + 25; 
        }
      }
    }
  }
  return 0; 
}

void UpdateDrawFrame(void)
{
  if (!block && IsMouseButtonDown(MOUSE_BUTTON_LEFT)) {
    Vector2 position = GetMousePosition(); 
    int code = keycode_from_xy(position.x, position.y); 
    if (code) {
      calc_on_key(code); 
      BeginDrawing();
      ClearBackground(RAYWHITE);
      DrawTexture(texture, 0, 0, WHITE);
      draw_screen(45, 58); 
      EndDrawing();
      block = 1; 
    }
  }
  if (IsMouseButtonUp(MOUSE_BUTTON_LEFT)) block = 0; 
  int key = GetKeyPressed(); 
  for (int i=0; i<49; i++) {
    int code = keymap[i]; 
    if (code && key == code) {
      calc_on_key(i); 
      BeginDrawing();
      ClearBackground(RAYWHITE);
      DrawTexture(texture, 0, 0, WHITE);
      draw_screen(45, 58); 
      EndDrawing();
    }
  }
}

int main(void)
{
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "basic window");

    Image image = LoadImage("resources/panel.png");
    texture = LoadTextureFromImage(image);
    UnloadImage(image);

    SetTargetFPS(20);
    BeginDrawing();
    report_voltage(2990); 
    sharp_clear(); 
    calc_init(); 
    ClearBackground(RAYWHITE);
    DrawTexture(texture, 0, 0, WHITE);
    draw_screen(45, 58); 
    EndDrawing();
    block = 0; 
    emscripten_set_main_loop(UpdateDrawFrame, 0, 1);
    CloseWindow();
    return 0;
}
