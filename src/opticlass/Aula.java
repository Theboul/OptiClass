package opticlass;

/**
 *
 * @author Usuario
 */
public class Aula {
    public int id;
    public int capacidad;

    public Aula(int id, int capacidad) {
        this.id = id;
        this.capacidad = capacidad;
    }

    public int getId() { return id; }
    public int getCapacidad() { return capacidad; }
}
