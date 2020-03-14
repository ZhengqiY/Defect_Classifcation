import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Please type String 1:");

        String s1 = sc.next();
        System.out.println("Please type String 2:");
        sc = new Scanner(System.in);
        String s2 = sc.next();

        IsStrOneToOne sol = new IsStrOneToOne();
        System.out.println(sol.isStrOneToOne(s1,s2));

    }
}
