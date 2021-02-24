import sys
import omero
import omero.cli
import omero.clients
from omero.gateway import BlitzGateway
from omero.model.enums import UnitsLength

if len(sys.argv) < 2:
    print("Usage: python set_pixel_size.py <project id>")
    sys.exit(1)

project_id = int(sys.argv[1])

def set_pixel_size(conn, img, x, y ,z):
    p = img.getPrimaryPixels()
    p.setPhysicalSizeX(omero.model.LengthI(x, UnitsLength.MICROMETER))
    p.setPhysicalSizeY(omero.model.LengthI(y, UnitsLength.MICROMETER))
    p.setPhysicalSizeZ(omero.model.LengthI(z, UnitsLength.MICROMETER))
    conn.getUpdateService().saveObject(p)
    print(f"Pixel size set to {x}x{y}x{z} for {img.getName()._val}")

with omero.cli.cli_login() as c:
    conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
    cs = conn.getContainerService()
    param = omero.sys.ParametersI().leaves()
    project = cs.loadContainerHierarchy("Project", [project_id], param)[0]
    for ds in project.linkedDatasetList():
        for img in ds.linkedImageList():
            if ds.getName()._val == "nGFP" and img.getName()._val == "TP_Chgreen":
                x = 0.33
            else:
                x = 0.38
            y = 0.33
            z = 2
            set_pixel_size(conn, img, x, y ,z)

