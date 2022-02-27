import java.util.Date;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import javax.xml.bind.DatatypeConverter;

public class Hasher {
    
    private static final String SECRET = "MaW5255Hx9HF4Tr4BW2M";

    private static final String FLAG = "magpie{tH15_b3tT3R_f**k1n9_w0Rk_p0p...}";
        
    private int serverNumber;
    private int numberOfServers;

    Hasher(int serverNumber, int numberOfServers) {
        this.serverNumber = serverNumber;
        this.numberOfServers = numberOfServers;
    }

    public HasherReturn getEncryptedData() {
        byte[] hashKey = this.getHash("key");
        String hashKeyHex = bytesToHex(hashKey);

        byte[] hashIV = this.getHash("iv");
        String hashIVHex = bytesToHex(hashIV).substring(0, 32);
       
        String hashSlice = this.splitHash(hashKeyHex);

        String ciphertext = "";
        try {
            ciphertext = AES.encrypt(FLAG, hashKey, Arrays.copyOfRange(hashIV, 0, 16));
        } catch (Exception e) {
            System.err.println("Error encrypting: " + e);
        }

        return new HasherReturn(ciphertext, hashSlice, hashIVHex);
    }

    private String splitHash(String hash) {
        /*
        Takes a hash and returns the corresponding substring based on
        the server number and total number of servers.
        */

        int sliceLength = hash.length() / this.numberOfServers;
        int modulus = hash.length() % this.numberOfServers;

        int start = sliceLength * this.serverNumber;

        String hashSlice = "";
        if (this.serverNumber != this.numberOfServers - 1) {
            hashSlice = hash.substring(start, start + sliceLength);
        } else {
            hashSlice = hash.substring(start, start + sliceLength + modulus);
        }

        return hashSlice;
    }

    private byte[] getHash(String type) {
        /*
        Rounds the current time to the nearest period, appends it with a secret,
        and hashes it.
        */

        // Get the current time in milliseconds.
        Date date = new Date();
        long currentTime = date.getTime();

        // Get the current time in milliseconds and round to the nearest period.
        long rounded = ((currentTime + (Server.keyPeriod - 1)) / Server.keyPeriod) * Server.keyPeriod;

        String toHash;

        if (type.equals("key")) {
            toHash = rounded + SECRET + "key";
        } else {
            toHash = rounded + SECRET + "iv";
        }

        // Hash the plain text key.
        byte[] encodedHash;
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            encodedHash = digest.digest(toHash.getBytes(StandardCharsets.UTF_8));
            
            return encodedHash;
        } catch (NoSuchAlgorithmException e) {
            System.err.println("Error hashing: " + e);
        }
        
        return null;
    }

    private static String bytesToHex(byte[] hash) {
        /*
        Converts a byte array to a hex string.
        */
        return DatatypeConverter.printHexBinary(hash);
    }
}