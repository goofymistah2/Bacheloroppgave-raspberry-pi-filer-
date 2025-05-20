#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>



volatile bool esp_flank_positive = 0;/*variabel som representerer systemtilstand*/


int en_pin_motor = 11; /*Motorpins*/
int in_pin_1_motor = 7; 
int in_pin_2_motor = 6;

int en_pin_magnet= 9;/*Magnetpins*/
int in_pin_1_magnet = 5; 
int in_pin_2_magnet= 8;

int end_switch_top = 3; /*Endebryterpins*/
int end_switch_bottom = 2; 

int esp_in_pin_1 = A1;
int esp_in_pin_2 = A2;
int esp_out_pin = A0;
int esp_inp_debounce_timer = false;
int esp_inp_debounce_time = 0;
int esp_inp_prev = 0;
int esp_inp = 0;

int state = 0; 

int input = 0; 




void onRise();

void setup() {
  Serial.begin(9600);
 
  pinMode(en_pin_motor,OUTPUT); 
  pinMode(in_pin_1_motor, OUTPUT); 
  pinMode(in_pin_2_motor,OUTPUT); 

  digitalWrite(en_pin_motor,LOW); 
  digitalWrite(in_pin_1_motor,LOW); 
  digitalWrite(in_pin_2_motor,LOW); 
  
  pinMode(en_pin_magnet,OUTPUT); 
  pinMode(in_pin_1_magnet, OUTPUT); 
  pinMode(in_pin_2_magnet,OUTPUT); 

  digitalWrite(en_pin_magnet,LOW);
  digitalWrite(in_pin_1_magnet,LOW);
  digitalWrite(in_pin_2_magnet,LOW);
  
  pinMode(end_switch_top, INPUT_PULLUP); 
  pinMode(end_switch_bottom, INPUT_PULLUP); 
  
  pinMode(esp_in_pin_1,INPUT);
  pinMode(esp_in_pin_2,INPUT);
  pinMode(esp_out_pin,OUTPUT);
  digitalWrite(esp_out_pin,LOW);

  
  

}


void motor_raise(){
  analogWrite(en_pin_motor,0); 
  delay(100);
  analogWrite(en_pin_motor,255); 
  digitalWrite(in_pin_1_motor,LOW); 
  digitalWrite(in_pin_2_motor,HIGH); 
  
}
void motor_lower(){
  analogWrite(en_pin_motor,0); 
  delay(100);
  analogWrite(en_pin_motor,255); 
  digitalWrite(in_pin_1_motor,HIGH); 
  digitalWrite(in_pin_2_motor,LOW);
  
}
void motor_stop(){
  analogWrite(en_pin_motor,0); 
  digitalWrite(in_pin_1_motor,LOW); 
  digitalWrite(in_pin_2_motor,LOW);
 
}
void motor_prevent_rotation(){
  analogWrite(en_pin_motor,79); 
  digitalWrite(in_pin_1_motor,LOW); 
  digitalWrite(in_pin_2_motor,HIGH);
  
}
void magnet_on(){
  analogWrite(en_pin_magnet,255); 
  digitalWrite(in_pin_1_magnet,HIGH); 
  digitalWrite(in_pin_2_magnet,LOW);
  
}
void magnet_drop(){
  analogWrite(en_pin_magnet,255); 
  digitalWrite(in_pin_1_magnet,LOW); 
  digitalWrite(in_pin_2_magnet,HIGH);
  }
void magnet_off(){
  analogWrite(en_pin_magnet,0); 
  digitalWrite(in_pin_1_magnet,LOW); 
  digitalWrite(in_pin_2_magnet,LOW);

}
void check_for_esp_inp(){
  int bit_one = digitalRead(esp_in_pin_1); 
  int bit_two = digitalRead(esp_in_pin_2);
  int esp_inp_temp = (bit_one<<1)|bit_two;
Serial.println(esp_inp_temp);
 if (((esp_inp_temp == 1) || (esp_inp_temp == 2)) && (!esp_inp_debounce_timer) && (esp_inp_temp!=esp_inp)){
    esp_inp_prev = esp_inp_temp; 
    esp_inp_debounce_timer = true;
    esp_inp_debounce_time = millis(); 
 }
 if (esp_inp_debounce_timer && (millis()-esp_inp_debounce_time)>100 && esp_inp_temp == esp_inp_prev){
  esp_inp = esp_inp_temp;
  esp_inp_debounce_timer = false;
  Serial.println("went through");
 }
 
}
void loop() {
check_for_esp_inp();
 Serial.print("state: "); 
 Serial.println(state);
 switch(state){
      case 0: 
     
      
        if (esp_inp==1){
          Serial.println("her");
      esp_flank_positive = false;
      state = 1;
      motor_lower();
    
    
     }
    break;
    
                           
      case 1: 
      
        
        
        if (digitalRead(end_switch_bottom)==LOW){
          
          motor_stop(); 
           magnet_on(); 
          delay(1000); 
          motor_raise(); 
          state = 2; 
        }
        break;
      case 2: 
       
        if (digitalRead(end_switch_top)==LOW){
          Serial.println("reached drop position");
          digitalWrite(esp_out_pin,HIGH);
          motor_prevent_rotation();
           
          state = 3;
        }
        break;
        
      case 3: 
       digitalWrite(esp_out_pin,HIGH);
        if (esp_inp == 2){
          
          magnet_drop(); 
          delay(500); 
          magnet_off(); 
          motor_stop();
          state = 0;
          digitalWrite(esp_out_pin,LOW);
          
        }
        break;
         

         
         
         
         
        
        

        
       
 
    }}
   
   
  
  
  
  // put your main code here, to run repeatedly:
  
  
