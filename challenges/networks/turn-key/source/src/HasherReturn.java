public class HasherReturn {

    public String ciphertext;
    public String partialKey;
    public String iv;

    HasherReturn(String ciphertext, String partialKey, String iv) {
        this.ciphertext = ciphertext;
        this.partialKey = partialKey;
        this.iv = iv;
    }
}