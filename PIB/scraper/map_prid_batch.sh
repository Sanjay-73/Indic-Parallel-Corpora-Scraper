#!/bin/bash

start_prid=1900000
end_prid=1970000
num_batches=10

batch_size=$(( (end_prid - start_prid) / num_batches ))

for ((batch = 0; batch < num_batches; batch++))
do
    batch_start=$((start_prid + batch * batch_size))
    batch_end=$((batch_start + batch_size - 1))

    if [ $batch_end -gt $end_prid ]
    then
        batch_end=$end_prid
    fi

    python map_prid_batch.py $batch_start $batch_end &
done
