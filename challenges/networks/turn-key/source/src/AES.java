import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.bind.DatatypeConverter;

public class AES{

    // convert string to byte array
    public static byte[] toByteArray(String s) {
        return DatatypeConverter.parseHexBinary(s);
    }

    // convert byte array to hex string
    public static String toHexString(byte[] array) {
        return DatatypeConverter.printHexBinary(array);
    }

    // 
    public static String encrypt(String plaintext, byte[] key, byte[] iv) throws 
        NoSuchPaddingException, NoSuchAlgorithmException,
        InvalidAlgorithmParameterException, InvalidKeyException,
        BadPaddingException, IllegalBlockSizeException,
        UnsupportedEncodingException {
    
        IvParameterSpec ivBytes = new IvParameterSpec(iv);
        SecretKeySpec skeySpec = new SecretKeySpec(key, "AES");
        
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, skeySpec, ivBytes);
        byte[] cipherText = cipher.doFinal(plaintext.getBytes());
        return toHexString(cipherText);
}

    public static String decrypt(String cipherText, byte[] key, byte[] iv)
        throws NoSuchPaddingException, NoSuchAlgorithmException,
        InvalidAlgorithmParameterException, InvalidKeyException,
        BadPaddingException, IllegalBlockSizeException,
        UnsupportedEncodingException {

        IvParameterSpec ivBytes = new IvParameterSpec(iv);
        SecretKeySpec skeySpec = new SecretKeySpec(key, "AES");

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, skeySpec, ivBytes);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText);
    }
}