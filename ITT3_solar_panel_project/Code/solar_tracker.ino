int topLeft;
int topRight;
int bottonLeft;
int bottomRight;
int Acceptable;

void setup() {
  Serial.begin(9600);
  pinMode (10, OUTPUT);
  pinMode (9, OUTPUT);
  pinMode (8, OUTPUT);
  pinMode (7, OUTPUT);
}


void loop() {
  //solar tracking 
  Acceptable = 20;
  topLeft = analogRead(A0);
  topRight = analogRead(A1);
  bottonLeft = analogRead(A2);
  bottomRight = analogRead(A3);

  // making average
  int avgtop = ((topLeft+topRight)/2);
  int avgbot = ((bottomRight+bottonLeft)/2);
  int avgleft = ((topLeft+bottonLeft)/2);
  int avgright = ((topRight+bottomRight)/2);
  
  Serial.println(avgtop);
  Serial.println(avgbot);
  Serial.println(avgleft);
  Serial.println(avgright);

  if (avgtop - avgbot > Acceptable){ 
    digitalWrite (10, HIGH);
    Serial.println("im going up");
    delay(100);
  }  
  else if (avgtop - avgbot < Acceptable){
    digitalWrite (10,LOW);
    Serial.println("top hit the mark");
    delay(100);
  }

  if(avgbot - avgtop > Acceptable){
    digitalWrite (9, HIGH);
    Serial.println("im going down");
    }  
  else if (avgbot - avgtop < Acceptable){
    digitalWrite (9,LOW);
    Serial.println("bottom hit the mark");
    delay(100);
  }

  if (avgright - avgleft > Acceptable){
    digitalWrite (8,HIGH);
    Serial.println("im going to the right");
    }  
  else if (avgright - avgleft < Acceptable){
    digitalWrite (8,LOW);
    Serial.println("Left hit the mark");
    delay(100);
  }

  if (avgleft - avgright > Acceptable){
  digitalWrite(7,HIGH);
  Serial.println("im going to the left");
  delay(100);
  }  
  else if (avgleft - avgright < Acceptable){
    digitalWrite (7,LOW);
    Serial.println("Right hit the mark");
    delay(100);
  } 
  
  delay(100);
}
