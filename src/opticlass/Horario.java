package opticlass;

/**
 *
 * @author Usuario
 */
public class Horario {
    public int id;
    public String bloque;

    public Horario(int id, String bloque) {
        this.id = id;
        this.bloque = bloque;
    }

    public int getId() { return id; }
    public String getBloque() { return bloque; }
}
