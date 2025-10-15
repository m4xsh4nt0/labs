package functionspoint;

public class TabulatedFunction {
    private FunctionsPoint[] points;
    private int pointsCount;
    
    
    public TabulatedFunction(double leftX, double rightX, int pCount) {
     pointsCount = pCount;
     points = new FunctionsPoint[pointsCount + 5];
     double step = (rightX - leftX)/(pointsCount - 1);
     for (int i = 0; i < pointsCount; i++){
        double x = leftX + i * step;
        points[i] = new FunctionsPoint(x,0.0);
        
     }
    }
    
    
    public TabulatedFunction(double leftX, double rightX, double[] values) {
        pointsCount = values.length;
        points = new FunctionsPoint[pointsCount + 5];
        double step = (rightX - leftX)/(pointsCount - 1);
        for(int i = 0; i < pointsCount; i++){
            double x = leftX + i * step;
            points[i] = new FunctionsPoint(x,values[i]);

        }
        
    }
    
    
    public double getLeftDomainBorder() {
        return points[0].getX();
    }
    
    public double getRightDomainBorder() {
        return points[pointsCount - 1].getX();
    }
    
    
     public double getFunctionValue(double x) {
        
       if (x < getLeftDomainBorder() || x > getRightDomainBorder()){
        throw new IndexOutOfBoundsException("Индекс выходит за границы");
       }
       for (int i = 0; i < pointsCount; i++){
        double x1 = points[i].getX();
        double x2 = points[i + 1].getX();
        if(x>=x1 && x<=x2){
            double y1 = points[i].getY();
            double y2 = points[i + 1].getY();
            double y = y1 + ((y2 - y1) / (x2 - x1)) * (x1 - x);
            return y;

        }
       }
       return Double.NaN;
      
        
        
    }
    
    
    public int getPointsCount() {
        return pointsCount;
    }
    
    public FunctionsPoint getPoint(int index) {
        if (index < 0 || index > pointsCount) {
            throw new IndexOutOfBoundsException("Индекс выходит за границы");
        }
        return points[index]; 
    }
    
    public void setPoint(int index, FunctionsPoint point) {
        if (index < 0 || index >= pointsCount) {
            throw new IndexOutOfBoundsException("Индекс выходит за границы");
        }
        
        if ( point.getX() <= points[index - 1].getX()) {
            return;
        }
        if ( point.getX() >= points[index + 1].getX()) {
            return;
        }
        
       points[index] = point;
    }
    
    public double getPointX(int index) {
        if (index < 0 || index >= pointsCount) {
            throw new IndexOutOfBoundsException("Индекс выходит за границы");
        }
        return points[index].getX();
    }
    
    public void setPointX(int index, double x) {
        if (index > 0 && index < pointsCount) {
        
        
        if (index > 0 && x <= points[index - 1].getX()) {
            return; 
        }
        if (index < pointsCount - 1 && x >= points[index + 1].getX()) {
            return; 
        }
        
        points[index].setX(x);
    }
    }
    
    public double getPointY(int index) {
        if (index < 0 || index >= pointsCount) {
            throw new IndexOutOfBoundsException("Индекс выходит за границы");
        }
        return points[index].getY();
    }
    
    public void setPointY(int index, double y) {
        if (index < 0 || index >= pointsCount) {
            throw new IndexOutOfBoundsException("Индекс выходит за границы");
        }
        points[index].setY(y);
    }
    
    
    public void deletePoint(int index) {
       if(index < 0 || index > pointsCount){
        throw new IndexOutOfBoundsException("Индекс выходит за границы");
       }
      System.arraycopy(points,index + 1,points,index,pointsCount - index - 1);
      pointsCount--;
    }
    
    public void addPoint(FunctionsPoint point) {
       FunctionsPoint[] nPoints = new FunctionsPoint[pointsCount + 10];
       System.arraycopy(points,0,nPoints,0,pointsCount);
       points = nPoints;
       int index = 0;
       while(point.getX() > points[index].getX() && index < pointsCount){
        index++;
       }
       if(point.getX() == points[index].getX()){
        points[index] = point;
        return;
       }
       System.arraycopy(points,index,points,index + 1,pointsCount - index);
       points[index] = point;
       pointsCount++;
    }
    public void printFunction() {
        System.out.println(" функция:");
        for (int i = 0; i < pointsCount; i++) {
            System.out.printf("Точка %d: (%.2f, %.2f)%n", i, points[i].getX(), points[i].getY());
        }
    
    
    }
}