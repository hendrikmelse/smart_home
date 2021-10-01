#include <Adafruit_NeoPixel.h>

#define RELAUNCH_V 0.5
#define ACCEL 0.03
#define BOUNCE 0.8
#define MIN_V 1.55
#define MAX_V 1.87

typedef struct {
  uint32_t color;
  double pos;
  double velocity;
} Particle;

class Bouncer {
public:
  Bouncer(Adafruit_NeoPixel *strip) {
    this->particles[0].color = 0xFF0000;
    this->particles[0].pos = 0;
    this->particles[0].velocity = 0;
    this->particles[1].color = 0x008000;
    this->particles[1].pos = 0;
    this->particles[1].velocity = 0;
    this->particles[2].color = 0x000090;
    this->particles[2].pos = 0;
    this->particles[2].velocity = 0;
    this->strip = strip;
  }

  void Next() {
    for (int i = 0; i < 3; ++i) {
      if (particles[i].pos <= 0) {
        // Particle fell below zero, decide what to do
        if (particles[i].velocity > -RELAUNCH_V) {
          // Particle going slow, relaunch it
          particles[i].velocity = random(int(MIN_V * 10000), int(MAX_V * 10000)) / 10000.0;
        }
        else {
          // Particle still going fast, bounce it
          particles[i].velocity *= -BOUNCE;
        }
        particles[i].pos = 0;
      }

      // Apply physics
      particles[i].pos += particles[i].velocity;
      particles[i].velocity -= ACCEL;

      this->strip->setPixelColor(max(min(int(particles[i].pos), 59), 0), particles[i].color);
    }
  }
  
private:
  Particle particles[3];
  Adafruit_NeoPixel *strip;
};
