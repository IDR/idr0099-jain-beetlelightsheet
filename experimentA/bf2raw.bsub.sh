#!/usr/bin/env bash
#BSUB -M 8192
#BSUB -R "rusage[mem=8192]"
#BSUB -n 8
#BSUB -o logs/b%I.out
#BSUB -e logs/b%I.err
#BSUB -J "images[1-4]"

# You must ensure the ~/logs directory exists before submitting this job
# mkdir -p ~/logs
# bsub < bf2raw.bsub
# bjobs

declare -A images
images[1]=16-4-15_LifeAct-eGFP/img_TL.tif.pattern
images[2]=4-3-15_nGFP/TP_Chgreen_Ill0_Ang0,1,2.tif.pattern
images[3]=8-6-19_ZenKD_GAP43-eYFP/fused_tp_ch_0.tif.pattern
images[4]=9-3-15_Histone-eGFP/TP_Chgreen_Ill0_Ang0,1,2.tif.pattern
#images[5]=22-06-16_Tc-Squash-eGFP/TP_Ch0_Ill0_Ang1,2,3,4,5.tif.pattern

. ~/miniconda3/bin/activate
conda activate idr0099-bioformats

set -eu
TOPDIR=idr0099-jain-beetlelightsheet/experimentA/patterns
OUTDIR=idr0099-jain-beetlelightsheet-zarr
IN="$TOPDIR/${images[$LSB_JOBINDEX]}"
OUT="$OUTDIR/${images[$LSB_JOBINDEX]}.zarr"
mkdir -p "$(dirname $OUT)"
echo bioformats2raw --file_type=zarr --max_workers=8 "$IN" "$OUT"
bioformats2raw --file_type=zarr --max_workers=8 "$IN" "$OUT"
