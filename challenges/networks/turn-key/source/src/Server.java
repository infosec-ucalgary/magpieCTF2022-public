import java.io.*;
import java.text.*;
import java.util.*;
import java.net.*;

public class Server {
    public static int serverPort;
    public static int serverNumber;
    public static int numberOfServers;

    public static long keyPeriod = 300;     // How often the key/iv get refreshed
    public static long protocolTime = 300;  // How long a client has to get the flag

    public void start() throws IOException {
        System.out.println("Starting server on port " + serverPort);

        ServerSocket ss = new ServerSocket(serverPort);

        while (true) {
            Socket s = null;

            try {
                s = ss.accept();
                System.out.println("A new client is connected: " + s);
            
                BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
                DataOutputStream out = new DataOutputStream(s.getOutputStream());
            
                Thread t = new ClientHandler(s, in, out);

                t.start();
            } catch (Exception e) {
                s.close();
            }
        }
    }

    public static void printUsage() {
        System.out.println("Usage: java Server <port> <serverNumber> <numberOfServers> [keyPeriod] [procotolTime]");
        System.exit(1);
    }

    public static void main(String args[]) {
        if (args.length >= 3) {
            try {
                serverPort = Integer.parseInt(args[0]);
                serverNumber = Integer.parseInt(args[1]);
                numberOfServers = Integer.parseInt(args[2]);
            } catch (NumberFormatException e) {
                printUsage();
            }
        } else {
            printUsage();
        }

        if (args.length >= 4) {
            try {
                keyPeriod = Long.parseLong(args[3]);
            } catch (NumberFormatException e) {
                printUsage();
            }
        }

        if (args.length >= 5) {
            try {
                protocolTime = Long.parseLong(args[4]);
            } catch (NumberFormatException e) {
                printUsage();
            }
        }

        Server server = new Server();
        
        try {
            server.start();
        } catch (IOException e) {
            System.err.println("Socket error: " + e);
        }
    }   
}