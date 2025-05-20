#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>



int active = 0;/*variabel som representerer systemtilstand*/
int state = 0;

int sda_pin = 22; /*Akselerometerpins*/
int scl_pin = 21;

int hall_pin = 32; 
int sample_time_list[600];
int sample_time_index = 0;
int arduino_in_pin = 25;
int arduino_out_pin_1 = 26;
int arduino_out_pin_2 = 27;
int prev_sampling_time =micros(); /*variabler for å begrense hvor ofte data samples fra akselerometer*/
int current_time = micros(); 
int sampling_interval=500; 
int time_at_drop;
int wait_until_sampling = 5;
int number_of_tests=1; 

int current_test_number = 1;

int accel_index = 0;

extern StaticJsonDocument<16384> doc; 
JsonArray z_accel;
JsonArray hall_data;




sensors_event_t event;
Adafruit_MMA8451 mma = Adafruit_MMA8451();

void mqtt_setup();
void mqtt_loop();
void publishJsonSimple();
void setup() {
  Serial.begin(115200);
  mqtt_setup();
  pinMode(arduino_out_pin_1,OUTPUT); 
  digitalWrite(arduino_out_pin_1,LOW);
  pinMode(arduino_out_pin_2,OUTPUT); 
  digitalWrite(arduino_out_pin_2,LOW);
  pinMode(arduino_in_pin,INPUT); 
  
  Wire.begin(sda_pin,scl_pin);
  
  mma.begin();
  
  mma.setRange(MMA8451_RANGE_8_G);

  z_accel = doc.createNestedArray("z_accel"); 
  hall_data = doc.createNestedArray("hall");

  

}


void loop() {
 if(state!=2){
  mqtt_loop();}

 switch(state){
      case 0: 
     
      
        if (active==1 && digitalRead(arduino_in_pin) == LOW){

       Serial.println("system activated");
      digitalWrite(arduino_out_pin_1, LOW);/*sender en puls til arduino*/
      digitalWrite(arduino_out_pin_2,HIGH);
      
      state = 1;
    
     }
    break;
    
      case 1: 
      if (digitalRead(arduino_in_pin)==HIGH){
        Serial.println("initiating drop");
      delay(500);
      digitalWrite(arduino_out_pin_1,HIGH);
      digitalWrite(arduino_out_pin_2,LOW);
     
      state = 2; 
      }
      break;
                 
        
      case 2: 
     
      
      current_time = micros();
      
      if ((current_time-prev_sampling_time)>=sampling_interval){
        
        
        z_accel.add(0);
        hall_data.add(analogRead(hall_pin));
        prev_sampling_time = current_time;
        accel_index +=1;
        
        
      }
      

      if(accel_index==1500){
        
        accel_index = 0;
          Serial.println("finished samling");
           publishJsonSimple();
           z_accel = doc.createNestedArray("z_accel"); 
           hall_data = doc.createNestedArray("hall");
          if (current_test_number>=number_of_tests){
            current_test_number = 1;
            active = 0;
            Serial.println("finished");
          }
          else{ /*begynn ny test*/
           
            current_test_number+=1;
            
            
          }
          for (int i = 0; i<600; i++){
            Serial.println(sample_time_list[i]);
          }
          
          state = 0;
          break; 
      }
      break;
        
         
         }
         

         
         
         
         
        
        

        
       
 
    }
   
   
