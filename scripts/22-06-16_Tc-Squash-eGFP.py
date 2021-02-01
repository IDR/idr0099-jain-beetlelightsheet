from ome_model import experimental as ome
import os
import tifffile

def create_companion(file_template, name, outdir, maxindex):
    os.makedirs(outdir, exist_ok=True)
    outpath = f'{outdir}/{name}.companion.ome'
    if os.path.isfile(outpath):
        print(f'{outpath} already exists, not overwriting')
        return

    for index in range(maxindex + 1):
        tif = file_template.format(index=index)
        if os.path.exists(tif):
            with tifffile.TiffFile(tif) as t:
                assert len(t.series) == 1
                s = t.series[0]
                assert s.axes == 'ZYX'
                t = index
                if index == 0:
                    z, y, x = s.shape
                    dt = str(s.dtype)
                    companion = ome.Image(
                        os.path.basename(name), x, y, z, 1, sizeT=(maxindex + 1),
                        order='XYZCT', type=dt)
                    companion.add_channel(samplesPerPixel=1)
                else:
                    assert s.shape == (z, y, x)
                    #assert str(s.dtype) == dt, (tif, index, dt)
                companion.add_tiff(os.path.basename(tif), t=t, planeCount=z)
        else:
            no_tif = tif
            tif = file_template.format(index=(index-1))
            if not os.path.exists(tif):
                tif = file_template.format(index=(index+2))
            if not os.path.exists(tif):
                print("{} doesn't exit, not substitute found.".format(no_tif))
                exit(1)
            print("{} doesn't exit, using {}".format(no_tif, tif))
            companion.add_tiff(os.path.basename(tif), t=t, planeCount=z)

        tifbase = os.path.basename(tif)
        tiflink = f'{outdir}/{tifbase}'
        if not os.path.islink(tiflink):
            os.symlink(tif, tiflink)

    with open(outpath, 'wb') as o:
        ome.create_companion(images=[companion], out=o)

parentdir = '/uod/idr/filesets/idr0099-jain-beetlelightsheet/20201001-ftp'
a = ('22-06-16_Tc-Squash-eGFP', 'TP{index}_Ch0_Ill0_Ang1,2,3,4,5.tif', 'TP_Ch0_Ill0_Ang1,2,3,4,5.tif', 212)
create_companion(f'{parentdir}/Akanksha_Jain_{a[0]}/{a[1]}', a[2], f'companions/{a[0]}', a[3])