public class Prime {
    public static boolean isPrime(int n) {
        String s = new String(new char[n]);
        System.out.println(s.length());
        return !s.matches(".?|(..+?)\\1+");
    }

    public static void main(String[] args) {
        System.out.println(Prime.isPrime(11));
    }
}
