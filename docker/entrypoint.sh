#!/bin/bash
# Customer Satisfaction Analytics - Docker Entrypoint
# Inicialización de servicios externos gratuitos

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo "🚀 Customer Satisfaction Analytics - External Services"
echo "💰 Cost: \$0.00 (Free Tier Only)"
echo "============================================="

# Verificar variables de entorno requeridas
check_env_vars() {
    log_info "Checking required environment variables..."
    
    REQUIRED_VARS=(
        "AWS_ACCESS_KEY_ID"
        "AWS_SECRET_ACCESS_KEY"
        "AWS_DEFAULT_REGION"
    )
    
    MISSING_VARS=()
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            MISSING_VARS+=("$var")
        fi
    done
    
    if [ ${#MISSING_VARS[@]} -ne 0 ]; then
        log_error "Missing required environment variables:"
        for var in "${MISSING_VARS[@]}"; do
            echo "  - $var"
        done
        log_info "Please set these variables or mount AWS credentials."
        return 1
    fi
    
    log_success "All required environment variables are set"
}

# Configurar AWS CLI
setup_aws() {
    log_info "Setting up AWS CLI..."
    
    # Configurar AWS CLI si no existe configuración
    if [ ! -f ~/.aws/credentials ]; then
        mkdir -p ~/.aws
        
        cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
EOF
        
        cat > ~/.aws/config << EOF
[default]
region = ${AWS_DEFAULT_REGION}
output = json
EOF
        
        log_success "AWS CLI configured"
    else
        log_info "AWS CLI already configured"
    fi
    
    # Verificar conectividad
    if aws sts get-caller-identity > /dev/null 2>&1; then
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        log_success "AWS connection verified (Account: $ACCOUNT_ID)"
    else
        log_error "Failed to connect to AWS"
        return 1
    fi
}

# Verificar recursos AWS (Free Tier)
check_aws_resources() {
    log_info "Checking AWS resources..."
    
    # Verificar buckets S3
    S3_BUCKETS=$(aws s3 ls | grep "customer-satisfaction" | wc -l)
    if [ "$S3_BUCKETS" -gt 0 ]; then
        log_success "Found $S3_BUCKETS S3 buckets"
    else
        log_warning "No S3 buckets found. Deploy infrastructure first."
    fi
    
    # Verificar Athena workgroup
    WORKGROUPS=$(aws athena list-work-groups --query "WorkGroups[?contains(Name, 'customer-satisfaction')].Name" --output text | wc -w)
    if [ "$WORKGROUPS" -gt 0 ]; then
        log_success "Found Athena workgroup"
    else
        log_warning "No Athena workgroup found. Deploy infrastructure first."
    fi
    
    # Verificar Glue database
    DATABASES=$(aws glue get-databases --query "DatabaseList[?contains(Name, 'customer_satisfaction')].Name" --output text | wc -w)
    if [ "$DATABASES" -gt 0 ]; then
        log_success "Found Glue database"
    else
        log_warning "No Glue database found. Deploy infrastructure first."
    fi
}

# Inicializar servicios según el comando
start_service() {
    case "$1" in
        "streamlit")
            log_info "Starting Streamlit dashboard..."
            cd /app/streamlit_dashboard
            
            # Actualizar configuración con recursos AWS reales
            if [ -f .env ]; then
                log_info "Loading environment configuration..."
                source .env
            fi
            
            # Obtener nombres reales de buckets si existen
            DATA_BUCKET=$(aws s3 ls | grep "customer-satisfaction-data-lake" | awk '{print $3}' | head -1)
            RESULTS_BUCKET=$(aws s3 ls | grep "customer-satisfaction-athena-results" | awk '{print $3}' | head -1)
            WORKGROUP=$(aws athena list-work-groups --query "WorkGroups[?contains(Name, 'customer-satisfaction')].Name" --output text | head -1)
            
            if [ ! -z "$DATA_BUCKET" ]; then
                export S3_DATA_BUCKET="$DATA_BUCKET"
                log_success "Using data bucket: $DATA_BUCKET"
            fi
            
            if [ ! -z "$RESULTS_BUCKET" ]; then
                export S3_RESULTS_BUCKET="$RESULTS_BUCKET"
                log_success "Using results bucket: $RESULTS_BUCKET"
            fi
            
            if [ ! -z "$WORKGROUP" ]; then
                export ATHENA_WORKGROUP="$WORKGROUP"
                log_success "Using Athena workgroup: $WORKGROUP"
            fi
            
            log_success "Starting Streamlit on port 8501..."
            exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0
            ;;
            
        "data-processor")
            log_info "Starting data processor..."
            cd /app
            
            # Ejecutar procesamiento de datos
            python scripts/data_processing.py
            
            # Mantener el contenedor vivo
            tail -f /dev/null
            ;;
            
        "cost-monitor")
            log_info "Starting cost monitor..."
            cd /app
            
            # Ejecutar monitor de costos cada hora
            while true; do
                log_info "Running cost check..."
                python scripts/aws_cost_monitor.py
                
                log_info "Sleeping for 1 hour..."
                sleep 3600
            done
            ;;
            
        "all")
            log_info "Starting all services..."
            
            # Iniciar Streamlit en background
            cd /app/streamlit_dashboard
            streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
            
            # Iniciar cost monitor
            cd /app
            while true; do
                python scripts/aws_cost_monitor.py
                sleep 3600
            done &
            
            # Mantener el contenedor vivo
            wait
            ;;
            
        *)
            log_error "Unknown service: $1"
            log_info "Available services: streamlit, data-processor, cost-monitor, all"
            exit 1
            ;;
    esac
}

# Función principal
main() {
    local service="${1:-streamlit}"
    
    log_info "Starting service: $service"
    
    # Verificaciones iniciales
    if ! check_env_vars; then
        exit 1
    fi
    
    if ! setup_aws; then
        exit 1
    fi
    
    check_aws_resources
    
    # Iniciar servicio
    start_service "$service"
}

# Manejo de señales para shutdown graceful
cleanup() {
    log_info "Shutting down gracefully..."
    exit 0
}

trap cleanup SIGTERM SIGINT

# Ejecutar función principal con argumentos
main "$@"
