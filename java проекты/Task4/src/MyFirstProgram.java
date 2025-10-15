class MyFirstClass {
    public static void main(String s[]){
    MySecondClass o = new MySecondClass(0,0);
   int i, j;
        for (i = 1; i <= 8; i++) {
            for (j = 1; j <= 8; j++) {
                o.set1(i);  
                o.set2(j); 
                System.out.print(o.addition()); 
                System.out.print(" ");
            }
            System.out.println();
        }
    }
}

class MySecondClass {
    private int i,j;

    
    public MySecondClass(int n1, int n2) {
        this.i = n1;
        this.j = n2;
    }

    public int get1() {
        return i;
    }
    public void set1(int firstNumber) {
        this.i = firstNumber;
    }
    public int get2() {
        return j;
    }
    public void set2(int secondNumber) {
        this.j = secondNumber;
    }

    public int addition() {
        return i + j;
    }
}

