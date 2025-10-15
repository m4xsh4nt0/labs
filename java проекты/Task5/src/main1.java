import functionspoint.*;

public class main1 {
    public static void main(String[] args) {
       double h[] = {0.0, 1.0, 2.0 , 3.0};
       TabulatedFunction n = new TabulatedFunction(0.0,3.0,h);
     n.addPoint(new FunctionsPoint(-1,1));
     n.addPoint(new FunctionsPoint(1.5,2.25));
      n.setPoint(3,new FunctionsPoint(2,7));
      n.setPointY(0,2);
      // n.deletePoint(3);
       for (int i = 0; i < n.getPointsCount(); i++){
        System.out.println(n.getPointX(i) + " " + n.getPointY(i));
        

       }
    }
}
        
        
        
        