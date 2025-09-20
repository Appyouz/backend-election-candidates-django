#!/bin/bash

# Import utility functions
source scripts/utils.sh

# Exit on any error
set -e

# Trap errors and show setup failed message
trap 'echo_error "❌ Setup failed! Exiting..."; exit 1' ERR

# Initialize variables
ENVIRONMENT=""
PYTHON_ALIAS=""

# Function to show usage
show_usage() {
    echo_info "Usage: $0 --env <dev|prod> --python_alias <python_command>"
    echo_info "Example: $0 --env dev --python_alias python3.11"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --python_alias)
            PYTHON_ALIAS="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            echo_error "Unknown option: $1"
            show_usage
            ;;
    esac
done

# Check if environment is provided
if [ -z "$ENVIRONMENT" ]; then
    echo_error "❌ Environment not provided. Please specify --env dev or --env prod"
    show_usage
fi

# Validate environment
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    echo_error "❌ Invalid environment. Must be 'dev' or 'prod'"
    show_usage
fi

# Check if python alias is provided
if [ -z "$PYTHON_ALIAS" ]; then
    echo_error "❌ Python alias not provided. Please specify --python_alias <python_command>"
    show_usage
fi

echo_info "🚀 Starting setup for $ENVIRONMENT environment..."

# Check if python alias is available
if ! command -v "$PYTHON_ALIAS" &> /dev/null; then
    echo_error "❌ Python command '$PYTHON_ALIAS' not found in system PATH"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_ALIAS --version 2>&1 | grep -oP '\d+\.\d+')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo_error "❌ Python version $PYTHON_VERSION is not supported. Required: Python >= 3.11"
    exit 1
elif [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -eq 11 ]; then
    echo_success "✅ Python version $PYTHON_VERSION is supported"
else
    echo_warning "⚠️  Python version $PYTHON_VERSION detected. Recommended: Python 3.11"
fi

# Handle environment-specific .env file
if [ "$ENVIRONMENT" = "dev" ]; then
    ENV_FILE=".env"
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example "$ENV_FILE"
            echo_success "✅ .env file created from .env.example"
        else
            echo_error "❌ .env.example file not found"
            exit 1
        fi
    else
        echo_info "ℹ️  .env file already exists, skipping copy"
    fi
else
    ENV_FILE=".env.prod"
    if [ ! -f "$ENV_FILE" ]; then
        echo_error "❌ .env.prod file not found for production environment"
        echo_error "   Please create .env.prod with production configuration using below command:"
        echo_info "   cp .env.example .env.prod"
        exit 1
    else
        echo_info "ℹ️  Using .env.prod for production environment"
    fi
fi

# Set DJANGO_DEBUG based on environment
if [ "$ENVIRONMENT" = "dev" ]; then
    export DJANGO_DEBUG=True
    echo_info "🔧 DJANGO_DEBUG set to True for development"
else
    export DJANGO_DEBUG=False
    echo_info "🔧 DJANGO_DEBUG set to False for production"
fi

# Function to read .env variables
get_env_var() {
    local var_name="$1"
    local var_value=$(grep "^${var_name}=" "$ENV_FILE" 2>/dev/null | cut -d '=' -f2- | sed 's/^["'\'']//' | sed 's/["'\'']$//')
    echo "$var_value"
}

# Check PostgreSQL connectivity
if [ -f "$ENV_FILE" ]; then
    echo_info "🔍 Checking database configuration in $ENV_FILE..."
    
    # Read database variables from .env
    DB_ENGINE=$(get_env_var "DJANGO_DB_ENGINE")
    DB_NAME=$(get_env_var "DJANGO_DB_NAME")
    DB_USER=$(get_env_var "DJANGO_DB_USER")
    DB_PASSWORD=$(get_env_var "DJANGO_DB_PASSWORD")
    DB_HOST=$(get_env_var "DJANGO_DB_HOST")
    DB_PORT=$(get_env_var "DJANGO_DB_PORT")
    
    # Check if database engine is PostgreSQL
    if [[ "$DB_ENGINE" != *"postgresql"* ]]; then
        echo_error "❌ Only PostgreSQL is supported. Found: $DB_ENGINE"
        echo_error "   Please update DJANGO_DB_ENGINE to use postgresql"
        exit 1
    fi
    
    # Validate required database credentials
    if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
        echo_error "❌ Database credentials incomplete in .env file"
        echo_error "   Required: DJANGO_DB_NAME and DJANGO_DB_USER"
        exit 1
    fi
    
    # Set default values if empty
    DB_HOST="${DB_HOST:-localhost}"
    DB_PORT="${DB_PORT:-5432}"
    
    # Check if psql is available
    if ! command -v psql &> /dev/null; then
        echo_error "❌ psql command not found. PostgreSQL client is required."
        echo_error "   Install postgresql-client package to continue"
        exit 1
    fi
    
    # Test PostgreSQL connection
    echo_info "   Testing connection to PostgreSQL..."
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; then
        echo_success "✅ PostgreSQL connection successful"
    else
        echo_error "❌ PostgreSQL connection failed"
        echo_error "   Host: $DB_HOST:$DB_PORT | Database: $DB_NAME | User: $DB_USER"
        echo_error "   Please verify:"
        echo_error "   • PostgreSQL server is running"
        echo_error "   • Database '$DB_NAME' exists"
        echo_error "   • User '$DB_USER' has access to the database"
        echo_error "   • Network connectivity to $DB_HOST:$DB_PORT"
        exit 1
    fi
else
    echo_error "❌ $ENV_FILE file is required for database configuration"
    exit 1
fi

echo_success "✅ .env setup done"

# Create static directory
if [ ! -d "static" ]; then
    mkdir -p static
    echo_success "✅ static/ directory created"
else
    echo_info "ℹ️  static/ directory already exists"
fi


# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo_success "✅ logs/ directory created"
else
    echo_info "ℹ️  logs/ directory already exists"
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo_info "📦 Creating virtual environment..."
    $PYTHON_ALIAS -m venv .venv
    echo_success "✅ Virtual environment created"
else
    echo_info "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo_info "🔄 Activating virtual environment..."
source .venv/bin/activate

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo_error "❌ Failed to activate virtual environment"
    exit 1
else
    echo_success "✅ Virtual environment activated: $VIRTUAL_ENV"
fi

# Install requirements
REQUIREMENTS_FILE="requirements/${ENVIRONMENT}.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo_error "❌ Requirements file not found: $REQUIREMENTS_FILE"
    exit 1
fi

echo_info "📚 Installing requirements from $REQUIREMENTS_FILE..."
pip install -r "$REQUIREMENTS_FILE"
echo_success "✅ Requirements installed successfully"

# Run migrations
echo_info "🔄 Running database migrations..."
$PYTHON_ALIAS manage.py migrate
echo_success "✅ Database migrations completed"

# Collect static files
echo_info "📁 Collecting static files..."
$PYTHON_ALIAS manage.py collectstatic --noinput
echo_success "✅ Static files collected"

# Display TODO information
echo_info "📋 TODO - Important reminders:"
echo_info "   • Activate virtual environment before running server: source .venv/bin/activate"
echo_info "   • Update .env file if any configuration changes are made"
echo_info "   • Run: $PYTHON_ALIAS manage.py setup_server"
echo_info "   • Restart celery workers if required"

# Show how to run development server
echo_info "🌐 To run local development server:"
echo_info "----------------------------------------------------"
echo_info "Activate virtual environment: source .venv/bin/activate"
echo_info "----------------------------------------------------"
echo_info "Set DJANGO_DEBUG: export DJANGO_DEBUG=True"
echo_info "----------------------------------------------------"
echo_info "   $PYTHON_ALIAS manage.py runserver localhost:8000"
echo_info "----------------------------------------------------"

echo_success "🎉 Setup complete! Environment: $ENVIRONMENT | Python: $PYTHON_VERSION"