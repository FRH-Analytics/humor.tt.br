import org.gicentre.utils.stat.*;
import org.gicentre.utils.move.*;

XYChart lineChart;

PVector valorMouseHover;
ZoomPan zoomer;

//variavel de controle do clique
int mes = 0;
String mesNome = "Mes1,Mes2 e Mes3";

final int  RESOLUCAO_X = 600;
final int RESOLUCAO_Y = 300;

float[]    mes1Dias;
float[]  mes1MediaHumor;
float[]  mes1Positivos;
float[]  mes1Negativos;

float[]    mes2Dias;
float[]  mes2MediaHumor;
float[]  mes2Positivos;
float[]  mes2Negativos;

float[]    mes3Dias;
float[]  mes3MediaHumor;
float[]  mes3Positivos;
float[]  mes3Negativos;

float[]    mesAllDias;
float[]  mesAllMediaHumor;
float[] mesAllPositivos;
float[] mesAllNegativos;

String[] dataMes1;
String[] dataMes2;
String[] dataMes3;

Circulo circuloHover;

class Circulo{
  
  float coordX;
  float coordY;
  int tamanho;
  
  
  void circuloDraw(){
    fill(180,50,50,100);
    smooth();
    ellipseMode(CENTER);
    ellipse(coordX, coordY, tamanho, tamanho);
  }
  
  void setTamanho(int tamanho){
    this.tamanho = tamanho;
  }
  
  void setPosicao(float eixoX, float eixoY){
    this.coordX = eixoX;
    this.coordY = eixoY;
  }
  
}

void setup()
{
  
  circuloHover = new Circulo();
  
  size(RESOLUCAO_X,RESOLUCAO_Y);
  smooth();
  zoomer = new ZoomPan(this);
  
  lineChart = new XYChart(this);
  
   
  dataMes1 = loadStrings("mes1.csv");
  mes1Dias = new float[dataMes1.length - 1];
  mes1MediaHumor = new float[dataMes1.length-1];
  mes1Positivos = new float[dataMes1.length-1];
  mes1Negativos = new float[dataMes1.length-1];

  dataMes2 = loadStrings("mes2.csv");
  mes2Dias = new float[dataMes2.length-1];
  mes2MediaHumor = new float[dataMes2.length-1];
  mes2Positivos = new float[dataMes2.length-1];
  mes2Negativos = new float[dataMes2.length-1];
  
  dataMes3 = loadStrings("mes3.csv");
  mes3Dias = new float[dataMes3.length - 1];
  mes3MediaHumor = new float[dataMes3.length-1];
  mes3Positivos = new float[dataMes3.length-1];
  mes3Negativos = new float[dataMes3.length-1];
  
  int tamanhoArrayTotal = (dataMes1.length -1) + (dataMes2.length-1) + (dataMes3.length-1);
  mesAllDias = new float[tamanhoArrayTotal];
  mesAllMediaHumor = new float[tamanhoArrayTotal];
  mesAllPositivos = new float[tamanhoArrayTotal];
  mesAllNegativos = new float[tamanhoArrayTotal];



  for(int i=0; i<dataMes1.length-1; i++){
    String[] tokens = dataMes1[i+1].split(",");
    mes1Dias[i] = Float.parseFloat(tokens[0]);
    mes1MediaHumor[i] = Float.parseFloat(tokens[1]);
    mes1Positivos[i] = Float.parseFloat(tokens[2]);
    mes1Negativos[i] = Float.parseFloat(tokens[3]);
    
    mesAllDias[i] = Float.parseFloat(tokens[0]);
    mesAllMediaHumor[i] = Float.parseFloat(tokens[1]);
    
  }

  for(int i=0; i<dataMes2.length-1; i++){
    String[] tokens = dataMes2[i+1].split(",");
    
    mes2Dias[i] = Float.parseFloat(tokens[0]);
    mes2MediaHumor[i] = Float.parseFloat(tokens[1]);
    mes2Positivos[i] = Float.parseFloat(tokens[2]);
    mes2Negativos[i] = Float.parseFloat(tokens[3]);
    
    mesAllDias[(dataMes1.length -1) + i] = (dataMes1.length - 1) + Float.parseFloat(tokens[0]);
    mesAllMediaHumor[(dataMes1.length -1) + i] = Float.parseFloat(tokens[1]);
    
  }


  for(int i=0; i<dataMes3.length-1; i++){
    String[] tokens = dataMes3[i+1].split(",");
    
    mes3Dias[i] = Float.parseFloat(tokens[0]);
    mes3MediaHumor[i] = Float.parseFloat(tokens[1]);
    mes3Positivos[i] = Float.parseFloat(tokens[2]);
    mes3Negativos[i] = Float.parseFloat(tokens[3]);
    
    mesAllDias[(dataMes1.length -1) + (dataMes2.length -1) + i] = (dataMes1.length -1) + (dataMes2.length -1) + Float.parseFloat(tokens[0]);
    mesAllMediaHumor[(dataMes1.length -1) + (dataMes2.length -1) + i] = Float.parseFloat(tokens[1]);
    
  }
    

  lineChart.setData(mesAllDias, mesAllMediaHumor);
  lineChart.showXAxis(true);
  lineChart.showYAxis(true);
  
  lineChart.setXAxisLabel("dias coletados");
  lineChart.setYAxisLabel("propoção de bom humor");
  
  lineChart.setMinY(0);
  lineChart.setMaxY(1);
  
  lineChart.setPointColour(color(180,50,50,100));
  lineChart.setPointSize(9);
  lineChart.setLineWidth(4);
    

}

void draw()
{
  
  background(255);
  smooth();
  fill(180,50,50,100);
  text("Humor do povo brasileiro no Twitter", 55.0, 15.0);
  text(mesNome, 55.0, 25.0);
  lineChart.draw(15,15,width-30,height-30);
  fill(120);
  
  valorMouseHover = lineChart.getScreenToData(new PVector(mouseX, mouseY));
    
  try{
   correcaoAposClick(valorMouseHover);
  
    //Se o mouse esta sob o primeiro mes
  if(valorMouseHover != null && valorMouseHover.x <= dataMes1.length){
    for(int i=0; i<dataMes1.length; i++){
      if(ehProximo(mes1MediaHumor[i], valorMouseHover.y)){
         int backgroudHoverQueryWidth;
         int backgroundHoverQueryHeight;
        
         circuloHover.setPosicao(mouseX,mouseY);
         for(int j=0; j<12; j++){
           circuloHover.setTamanho(j);
            circuloHover.circuloDraw();
         }
        
        
        //Colocar coordenada certa para o texto
        fill(254, 230, 206);
        String hoverQueryValue = " Pos: "+(int(mes1Positivos[i]))+"\n"+" Neg: "+(int(mes1Negativos[i]));
        backgroudHoverQueryWidth = 1*100;
        backgroundHoverQueryHeight = -15;
        smooth(2);
        stroke(255,255,255);
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight*-1);
               
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight);
        fill(0,0,0);
        text(hoverQueryValue, mouseX,mouseY-23);
       break; 
      }
    }
  }
  
  //Se o mouse esta sob o segundo mes
  else if(valorMouseHover != null && (valorMouseHover.x > dataMes1.length) && valorMouseHover.x <= (dataMes1.length + dataMes2.length)){
    for(int i=0; i<dataMes2.length; i++){
      if(ehProximo(mes2MediaHumor[i], valorMouseHover.y)){
         int backgroudHoverQueryWidth;
         int backgroundHoverQueryHeight;
        
         //circulo que acompanha o hover
         circuloHover.setPosicao(mouseX,mouseY);
         for(int j=0; j<10; j++){
           circuloHover.setTamanho(j);
            circuloHover.circuloDraw();
         }
       
        
        //Colocar coordenada certa para o texto
        fill(254, 230, 206);
        String hoverQueryValue = " Pos: "+(int(mes2Positivos[i]))+"\n"+" Neg: "+(int (mes2Negativos[i]));
        backgroudHoverQueryWidth = 1*100;
        backgroundHoverQueryHeight = -15;
        smooth(1000);
        stroke(255,255,255);
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight*-1);
               
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight);
        fill(0, 0, 0);
        text(hoverQueryValue, mouseX,mouseY-23);
       break; 
      }
    }
  }
  //Se o mouse esta sob o terceiro mes
  else{
    for(int i=0; i<dataMes3.length; i++){
      if(ehProximo(mes3MediaHumor[i], valorMouseHover.y)){
        
         int backgroudHoverQueryWidth;
         int backgroundHoverQueryHeight;
        
         //circulo que acompanha o hover
         circuloHover.setPosicao(mouseX,mouseY);
         for(int j=0; j<12; j++){
           circuloHover.setTamanho(j);
            circuloHover.circuloDraw();
         }
        
        //Colocar coordenada certa para o texto
        fill(254, 230, 206);
        smooth(2);
        String hoverQueryValue = " Pos: "+(int (mes3Positivos[i]))+"\n"+" Neg: "+(int (mes3Negativos[i]));
        stroke(255,255,255);
        backgroudHoverQueryWidth = 1*100;
        backgroundHoverQueryHeight = -15;
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight*-1);
               
        rect(mouseX, mouseY-20, backgroudHoverQueryWidth, backgroundHoverQueryHeight);
        fill(0, 0, 0);
        text(hoverQueryValue, mouseX,mouseY-23);
       break; 
      }
    }
  } 
  }catch(Exception e){
    System.out.println(e.getMessage());
  }
   
}

double arredondar(double valor, int casas, int ceilOrFloor) {  
      double arredondado = valor;  
      arredondado *= (Math.pow(10, casas));  
      if (ceilOrFloor == 0) {  
         arredondado = Math.ceil(arredondado);           
      } else {  
         arredondado = Math.floor(arredondado);  
      }  
      arredondado /= (Math.pow(10, casas));  
      return arredondado;  
}

void correcaoAposClick(PVector p){
  if(mes == 2){
   p.x += dataMes1.length;
  }else if(mes == 3){
    p.x += dataMes1.length + dataMes2.length;
  }else{
    p.x += 0;
  }
}

boolean ehProximo(float valor1, float valor2){
  double valorCompara1 = arredondar(valor1,2,0);
  double valorCompara2 = arredondar(valor2,2,0);
  
  return valorCompara1 == valorCompara2;
}

void mousePressed(){
  
  //muda os labels
  lineChart.setXAxisLabel("dia");
    
  //Verificar em qual mes o cara clicou e dar o zoom nesse mes
  
  PVector mouse = lineChart.getScreenToData(new PVector(mouseX, mouseY));
  
  //Clicando com o botao direito volta pra visao geral
  if(mouseButton == RIGHT){
    lineChart.setData(mesAllDias, mesAllMediaHumor);
    mes = 0;
    lineChart.setXAxisLabel("dias coletados");
    mesNome="Mes1,Mes2 e Mes3";
  
  //Com o botao esquerdo da zoom no mes  
  }else if(mouseButton == LEFT && mes == 0){
  
    if(mouse.x <= mes1Dias.length){
      lineChart.setData(mes1Dias, mes1MediaHumor);
      mes = 1;
      mesNome = "Mes1";
      
    }else if(mouse.x > (mes1Dias.length) && mouse.x <= (mes1Dias.length + mes2Dias.length)){
      lineChart.setData(mes2Dias, mes2MediaHumor);
      mes = 2;
      mesNome = "Mes2";
      
    }else{
      lineChart.setData(mes3Dias, mes3MediaHumor);
      mes = 3;
      mesNome = "Mes3";
    }
  
  }
  
    
}


