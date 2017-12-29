# Dockerfile to run OSU benchmarks with Batch Shipyard on Azure Batch

FROM nvidia/cuda:8.0-devel-centos7
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install base system.
COPY ssh_config /root/.ssh/config
RUN yum update && \
    # Batch Shipyard dependencies.
    yum install -y openssh-server openssh-clients && \
    # InfiniBand/RDMA dependencies.
    yum install -y cpio libmlx4 libmlx5 librdmacm libmthca dapl dapl-utils && \
    # OSU-benchmarks dependencies.
    yum install -y wget gcc gcc-c++ make && \
    # Configure ssh server and keys.
    mkdir -p /var/run/sshd && \
    ssh-keygen -A && \
    sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#RSAAuthentication yes/RSAAuthentication yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' && \
    chmod 600 /root/.ssh/config && \
    chmod 700 /root/.ssh && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Install Intel MPI Library.
COPY l_mpi_2017.2.174.tgz /tmp/
RUN cd /tmp && \
    tar -xzf l_mpi_2017.2.174.tgz && \
    cd l_mpi_2017.2.174 && \
    sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' silent.cfg && \
    sed -i -e 's/^ARCH_SELECTED=ALL/ARCH_SELECTED=INTEL64/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    cd /tmp && \
    rm -rf l_mpi_2017.2.174 l_mpi_2017.2.174.tgz

# Install the OSU MPI benchmarks.
RUN source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    OSU_VERSION=5.3.2 && \
    OSU_TARBALL=osu-micro-benchmarks-${OSU_VERSION}.tar.gz && \
    OSU_URL=http://mvapich.cse.ohio-state.edu/download/mvapich/${OSU_TARBALL} && \
    wget ${OSU_URL} -P /tmp && \
    OSU_DIR=/opt/osu-micro-benchmarks/${OSU_VERSION} && \
    mkdir -p ${OSU_DIR} && \
    tar -xzf /tmp/${OSU_TARBALL} -C ${OSU_DIR} --strip-components=1 && \
    cd ${OSU_DIR} && \
    ./configure --prefix=/usr/local \
        CC=mpicc \
        CXX=mpicxx \
        --enable-cuda \
        --with-cuda=/usr/local/cuda-8.0 && \
    make -j"$(nproc)" install && \
    ldconfig /usr/local/lib && \
    rm -f /tmp/${OSU_TARBALL}

# Remove Intel components (runtime will be mounted from the host).
RUN rm -rf /opt/intel

# Set sshd command.
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
