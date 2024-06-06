#include <MicroNMEA.h>

#include<stdio.h>
#include<string.h>
#include <SD.h>

#define DEBUG true
  int pon=9;
  int poff=6;
  int lowp=5;

File logFile;
int inicial =1, count=0;
float flat, flon, flat2, flon2;  
char nmeaBuffer[100];
MicroNMEA nmea(nmeaBuffer, sizeof(nmeaBuffer));

void setup()
{

  pinMode(pon, OUTPUT);
  pinMode(poff, OUTPUT);
  pinMode(lowp, OUTPUT);
  digitalWrite(poff, LOW);
  digitalWrite(lowp, HIGH);   
  digitalWrite(pon, HIGH);
  SerialUSB.begin(115200);
   /*while (!SerialUSB) {
    ; // wait for serial port to connect
  }*/
  Serial1.begin(115200); 
  digitalWrite(pon, LOW);    
  delay(3000); 
  digitalWrite(pon, HIGH);
  delay(5000); 
  sendData("AT+GPS=1 ",1000,DEBUG);

  //Tarjeta SD
  SerialUSB.print(F("Iniciando SD ..."));
  if (!SD.begin(4))
  {
    SerialUSB.println(F("Error al iniciar"));
    return;
  }
  SerialUSB.println(F("Iniciado correctamente"));
}

void loop()
{
    String respuesta="";

    // Abrir archivo y escribir valor
    logFile = SD.open("datalog.txt", FILE_WRITE);
    if (inicial==1) {
      logFile.println("FECHA,HORA,LAT,LON,VEL,ALT,DST");
      inicial=0;   
    }    
    
    sendData("AT+GPSRD=1",1000,DEBUG);
    //delay(500);



    // Output GPS information from previous second
    SerialUSB.print("Valid fix: ");
    SerialUSB.println(nmea.isValid() ? "yes" : "no");

    SerialUSB.print("Nav. system: ");
    if (nmea.getNavSystem())
      SerialUSB.println(nmea.getNavSystem());
    else
      SerialUSB.println("none");

    SerialUSB.print("Num. satellites: ");
    SerialUSB.println(nmea.getNumSatellites());
    SerialUSB.print("HDOP: ");
    SerialUSB.println(nmea.getHDOP()/10., 1);

    SerialUSB.print("Date/time: ");
    SerialUSB.print(nmea.getYear());
    SerialUSB.print('-');
    SerialUSB.print(int(nmea.getMonth()));
    SerialUSB.print('-');
    SerialUSB.print(int(nmea.getDay()));
    SerialUSB.print('T');
    SerialUSB.print(int(nmea.getHour()));SerialUSB.print(':');SerialUSB.print(int(nmea.getMinute()));SerialUSB.print(':');SerialUSB.println(int(nmea.getSecond()));

    long latitude_mdeg = nmea.getLatitude();
    long longitude_mdeg = nmea.getLongitude();
    SerialUSB.print("Latitude (deg): ");SerialUSB.println(latitude_mdeg / 1000000., 6);SerialUSB.print("Longitude (deg): ");SerialUSB.println(longitude_mdeg / 1000000., 6);

    long alt;
    SerialUSB.print("Altitude (m): ");
    if (nmea.getAltitude(alt))
      SerialUSB.println(alt / 1000., 3);
    else
      SerialUSB.println("not available");

    SerialUSB.print("Speed: ");SerialUSB.println(nmea.getSpeed() / 1000., 3);SerialUSB.print("Course: ");SerialUSB.println(nmea.getCourse() / 1000., 3);



// Escribir en el archivo ("LAT,LON,VEL,ALT,DST");
    if (logFile) { 
      logFile.print(nmea.getYear());logFile.print('/');logFile.print(int(nmea.getMonth()));logFile.print('/');logFile.print(int(nmea.getDay()));
      logFile.print(",");    
      logFile.print(int(nmea.getHour()));logFile.print(':');logFile.print(int(nmea.getMinute()));logFile.print(':');logFile.print(int(nmea.getSecond()));
      logFile.print(",");
      logFile.print(latitude_mdeg / 1000000., 6);
      logFile.print(",");
      flat=longitude_mdeg/1000000.;
      logFile.print(longitude_mdeg / 1000000., 6);
      flon=longitude_mdeg / 1000000.;
      logFile.print(",");
      logFile.print(nmea.getCourse() / 1000., 3);
      logFile.print(",");
      logFile.print(alt / 1000., 3);
      logFile.print(",");
      logFile.println(haversine(flat,flon,flat2,flon2));
      logFile.close();

      if ( count++ >64 )      // Este numero controla cada cuantas lecturas escribimos
         {                    // No escribais demasiado a menudo, darle al menos 64/128
           logFile.flush();   // Para forzar la escritura en la SD
            count = 0 ;       
         }
      //logFile.close();
      SerialUSB.print("Dst: ");SerialUSB.println(haversine(flat,flon,flat2,flon2));
    } 
    else {
      SerialUSB.println("Error al abrir el archivo");
    }   
    flat2=flat;
    flon2=flon;
  
}


String sendData(String command, const int timeout, boolean debug)
{
    String response = "";    
    Serial1.println("Comando recibido->" + command); 
    long int time = millis();   
    while( (time+timeout) > millis())
    {
      while(Serial1.available())
      {       
        char c = Serial1.read(); 
        nmea.process(c);
        response+=c;
      }  
    }    
    if(debug)
    {
      //SerialUSB.print(response);
    }    
    return response;
}

double haversine(double lat1, double lon1, double lat2, double lon2) {
    const double rEarth = 6371000.0; // in meters
    double x = pow( sin( ((lat2 - lat1)*M_PI/180.0) / 2.0), 2.0 );
    double y = cos(lat1*M_PI/180.0) * cos(lat2*M_PI/180.0);
    double z = pow( sin( ((lon2 - lon1)*M_PI/180.0) / 2.0), 2.0 );
    double a = x + y * z;
    double c = 2.0 * atan2(sqrt(a), sqrt(1.0-a));
    double d = rEarth * c;
    // Serial.printlnf("%12.9f, %12.9f, %12.9f, %12.9f, %12.9f, %12.9f", x, y, z, a, c, d);
    return d; // in meters
}
