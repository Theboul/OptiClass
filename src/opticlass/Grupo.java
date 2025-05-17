package opticlass;

/**
 *
 * @author Usuario
 */
public class Grupo {
    public int id;
    public int cantidadEstudiantes;
    public String materia;

    public Grupo(int id, int cantidadEstudiantes, String materia) {
        this.id = id;
        this.cantidadEstudiantes = cantidadEstudiantes;
        this.materia = materia;
    }

    public int getId() { return id; }
    public int getCantidadEstudiantes() { return cantidadEstudiantes; }
    public String getMateria() { return materia; }
}
