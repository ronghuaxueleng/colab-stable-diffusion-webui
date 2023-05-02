mkdir -p /usr/local/envs/stablediffusion
tar -xzvf /content/drive/MyDrive/conda/stablediffusion.tar.gz -C /usr/local/envs/stablediffusion
/usr/local/bin/conda init
source /usr/local/etc/profile.d/conda.sh activate stablediffusion
source /usr/local/etc/profile.d/conda.sh deactivate
conda activate stablediffusion
source /usr/local/envs/stablediffusion/bin/activate
python --version