public class OrderConfirmation {
    public static void main(String[] args) {
        StringBuilder message = new StringBuilder("Order confirmed successfully! Thank you for shopping at Perfume Palace.\nOrder Details:\n");
        if (args.length > 0) {
            message.append(args[0]);
        } else {
            message.append("No items in order.");
        }
        System.out.println(message.toString());
    }
}