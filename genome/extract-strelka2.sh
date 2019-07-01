#!/bin/bash
SAMPLE=$1

for VCF in $(ls *$SAMPLE*/results/variants/variants.vcf.gz)
do
    NEW=${VCF/\/variants.vcf.gz/.strelka2.variants.vcf.gz}
    NEW=${NEW/\/results\/variants/}
    echo "$VCF --> $NEW"
    mv $VCF $NEW
done
