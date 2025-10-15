 class FunctionsPoint {
    public static void main(){}
    private double x,y;

    
    public FunctionsPoint(double n1, double n2) {
        this.x = n1;
        this.y = n2;
    }
    public FunctionsPoint(){
        x = 0;
        y = 0;
    }
    public FunctionsPoint(FunctionsPoint point){
        x = point.x;
        y = point.y;
    }
    public double getX() {
        return x;
    }
    public void setX(double cx) {
        this.x = cx;
    }
    public double getY() {
        return y;
    }
    public void setY(double cy) {
        this.y = cy;
    }

    
}