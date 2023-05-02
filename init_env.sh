/usr/local/bin/conda init
source /usr/local/etc/profile.d/conda.sh activate stablediffusion
source /usr/local/etc/profile.d/conda.sh deactivate
conda activate stablediffusion
python --version
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip install -q torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 torchtext==0.14.1 torchdata==0.5.1 --extra-index-url https://download.pytorch.org/whl/cu116 -U
pip install -q xformers==0.0.16 triton==2.0.0 -U
source /usr/local/etc/profile.d/conda.sh deactivate
rm -rf /content/drive/MyDrive/conda/stablediffusion.tar.gz
conda pack -n stablediffusion -o /content/drive/MyDrive/conda/stablediffusion.tar.gz
ls -lh /content/drive/MyDrive/conda/stablediffusion.tar.gz