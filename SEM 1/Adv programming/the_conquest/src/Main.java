public class Main{

    public static class Apple{
        String color;
        int weight;

        public void display(){
            System.out.println(color+'\n'+weight);
        }
    }

    public static void main(String[] args) {

        Apple adf = new Apple();
        Apple adf2 = new Apple();
        adf.color = "Blue";
        adf.weight = 100;
        adf2 = adf;
        adf2.display();
    }
}