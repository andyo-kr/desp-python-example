#!/bin/bash

while getopts n:t:d:o:e: flag
do
    case "${flag}" in
        n) namespace=${OPTARG};;
        e) environment=${OPTARG};;
        t) topic=${OPTARG};;
        d) date=${OPTARG};;
        o) destination_dir=${OPTARG};;
    esac
done

if [ -z "$namespace" ] || [ -z "$environment" ] || [ -z "$topic" ] || [ -z "$date" ] || [ -z "$destination_dir" ]; then
        echo 'Must include all parameters: -n namespace_name (ex: krogercustomer) -e environment (ex: stage | prod) -t topic (ex: enterprise_payments) -d (ex: 2021-02-02) -o destination_dir (ex: data)' >&2
        exit 1
fi

name="${namespace}-${environment}-${topic}"

subscription="DataManagementPlatformNonProd"
account_name="dmpdatalakelandingtest"

if [ $environment == "prod" ]; then
    subscription="DataManagementPlatformProd"
    account_name="dmpdatalakelanding"
fi

list_files=`az storage blob list --auth-mode login --container-name desp --account-name $account_name --subscription $subscription --prefix ${name}/${date} | grep name | grep avro | awk -F '"' '{print $4}'`

num_files=`echo "$list_files" | wc -l`

echo "Number of files to download: $num_files"

mkdir ${destination_dir}/${name}
mkdir ${destination_dir}/${name}/${date}

count=0

while IFS= read -r line; do
    az storage blob download --auth-mode login --container-name desp --name ${line} --file data/${line} --account-name $account_name --subscription $subscription
    count=$((count+1))
    echo "**************** Finished downloading $count files out of $num_files total. ****************"
done <<< "$list_files"
