package functionspoint;

public class FunctionsPoint {
    private double x;
    private double y;

    // Конструктор с заданными координатами
    public FunctionsPoint(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // Конструктор копирования
    public FunctionsPoint(FunctionsPoint point) {
        this.x = point.x;
        this.y = point.y;
    }

    // Конструктор по умолчанию
    public FunctionsPoint() {
        this(0.0, 0.0);
    }

    // Геттеры и сеттеры
    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }
}