import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


def plot_ca_scatter(structure, output_path: str) -> None:
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    xs, ys, zs = [], [], []
    for atom in structure.get_atoms():
        if atom.get_id() == "CA":
            x, y, z = atom.get_coord()
            xs.append(x)
            ys.append(y)
            zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=10, c="teal", alpha=0.8)
    ax.set_title("C-alpha 3D Scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_ramachandran(angles: list, output_path: str) -> None:
    phis = [a[0] for a in angles]
    psis = [a[1] for a in angles]
    plt.figure()
    plt.scatter(phis, psis, s=5, c="darkorange", alpha=0.7)
    plt.title("Ramachandran Plot")
    plt.xlabel("Phi (°)")
    plt.ylabel("Psi (°)")
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
