import java.io.*;
import java.text.*;
import java.util.*;
import java.net.*;
import java.nio.charset.Charset;

class ClientHandler extends Thread {

    final BufferedReader in;
    final DataOutputStream out;
    final Socket s;

    public ClientHandler(Socket s, BufferedReader in, DataOutputStream out) {
        this.s = s;
        this.in = in;
        this.out = out;
    }

    @Override
    public void run() {
        Hasher h = new Hasher(Server.serverNumber, Server.numberOfServers);
        HasherReturn hr = h.getEncryptedData();

        Date date = new Date();
        long startTime = date.getTime();

        // Do protocol

        String received;

        // Step 0: Server acknowledges connection
        send("Oh, hai!\n");

        // Step 1: Client sends initialization message
        received = receive();
        if(!received.equals("INITIALIZE CONNECTION")) {
            send("Invalid connection intialization. Terminating connection\n");
            closeSocket();
            return;
        }
        
        // Step 2: Server responds with acknowledgment
        send("Connection successfully initialized. Please reply with request...\n");

        // Step 3: Client requests flag
        received = receive();
        if(!received.equals("SEND FLAG")) {
            send("Invalid request. Terminating connection\n");
            closeSocket();
            return;
        }
        
        // Step 5: Server challenges with...random string reply?
        String randomString = getRandomString(7);
        send("Flag requested. Reply with challenge string " + randomString + "\n");

        // Step 6: Client sends random string reply
        received = receive();
        if(!received.equals(randomString)) {
            send("Challenge failed. Terminating connection\n");
            closeSocket();
            return;
        }

        // Step 7: If correct reply, send flag piece, else too late...
        date = new Date();
        long endTime = date.getTime();
        long diff = endTime - startTime;

        if (diff > Server.protocolTime) {
            failed(diff);
        } else {
            succeeded(diff, hr);
        }

        closeSocket();

        return;
    }

    private void closeSocket() {
        try {
            s.close();
        } catch (IOException e) {
            System.err.println("Error closing socket: " + e);
        }
    }

    private void failed(long diff) {
        // Took too long.
        String toSend = "Sorry, too slow! Your request took " + diff + "ms! The protocol must be completed in under " + Server.protocolTime + "ms!\n";
        toSend += "The flag encryption rotates every on all " + Server.numberOfServers + " servers every " + Server.keyPeriod + "ms.\n";

        send(toSend);
    }

    private void succeeded(long diff, HasherReturn hr) {
        // Send the encrypted flag.
        String toSend = "Success! Your request took " + diff + "ms!";
        toSend += "\nThe flag encryption rotates every on all " + Server.numberOfServers + " servers every " + Server.keyPeriod + "ms.";
        toSend += "\n\nAES-256 (CBC PKCS5)";
        toSend += "\nPartial key (" + (Server.serverNumber + 1) + "/" + Server.numberOfServers + "): 0x" + hr.partialKey;
        toSend += "\nIV: 0x" + hr.iv;
        toSend += "\nCiphertext: 0x" + hr.ciphertext;
        toSend += "\n";

        send(toSend);
    }

    private void send(String toSend) {
        try {
            this.out.writeBytes(toSend);
            this.out.flush();
        } catch (IOException e) {
            System.err.println("Error writing to socket: " + e);
        }
    }

    private String receive() {
        String received = "";
        try {
            received = this.in.readLine();
        } catch (IOException e) {
            System.err.println("Error reading from socket: " + e);
        }
        return received;
    }

    private String getRandomString(int length) {
        String SALTCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        StringBuilder salt = new StringBuilder();
        Random rnd = new Random();
        while (salt.length() < length) { // length of the random string.
            int index = (int) (rnd.nextFloat() * SALTCHARS.length());
            salt.append(SALTCHARS.charAt(index));
        }
        String saltStr = salt.toString();
        return saltStr;
    }

}