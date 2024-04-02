#!/bin/bash

if [ $# -ne 1 ] && [ $# -ne 2 ]; then
    echo ""
    echo "Usage: $0 <target_domain> [output_directory]"
    echo ""
    echo "Examples:"
    echo "  subscan example.com"
    echo "  subscan example.com example_folder"
    echo ""
    echo "If output_directory is not provided, it defaults to the target_domain name"
    
    exit 1
fi

domain=$1
output_dir=${2:-$domain}

# handle errors
handle_error() {
    echo -e "\033[1m\033[31mError: $1\033[0m"
    exit 1
}

# check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1 || handle_error "Command '$(basename "$1")' not found. Please make sure it's installed."
}

print_info() {
    echo -e "[""\033[34mINF\033[0m""]" $1
}

print_ok() {
    echo -e "[""\033[32mOK\033[0m""]" "$1"
}

print_success() {
    echo -e "[""\033[32mYay\033[0m""]" "$1"
}

# Check if required commands exist
command_exists "gau"
command_exists "waybackurls"
command_exists "subfinder"
command_exists "httpx"
command_exists "unfurl"

# create directory to save subdomains
if [ -d "$output_dir" ]; then
    while true; do
        read -p "Directory $output_dir already exists. Please enter a different name for the output directory: " new_output_dir
        if [ -z "$new_output_dir" ]; then
            echo "Please provide a valid directory name."
        elif [ -d "$new_output_dir" ]; then
            echo "Directory $new_output_dir already exists. Please choose a different name."
        else
            output_dir=$new_output_dir
            break
        fi
    done
fi

mkdir -p "$output_dir"
mkdir -p "$output_dir/scan_output"
echo ""
print_info "Directory $output_dir created"
echo ""

# Use gau to find subdomains and save to gau.txt
print_info "Scanning with gau"
"gau" --subs "$domain" 2>/dev/null | "unfurl" domains >> "$output_dir/scan_output/gau.txt" || handle_error "Failed to run gau."
print_ok "Scan with gau completed"

echo ""

# Use waybackurls to find subdomains and save to waybackurls.txt
print_info "Scanning with waybackurls"
"waybackurls" "$domain" | "unfurl" domains >> "$output_dir/scan_output/waybackurls.txt" || handle_error "Failed to run waybackurls."
print_ok "Scan with waybackurls completed"

echo ""

# Use subfinder to find subdomains and save to subfinder.txt
print_info "Scanning with Subfinder"
"subfinder" -d "$domain" -silent >> "$output_dir/scan_output/subfinder.txt" || handle_error "Failed to run subfinder."
print_ok "Scan with Subfinder completed"

echo ""

# Remove duplicate subdomains and save to subdomains.txt
print_info "Removing duplicate subdomains"
cat "$output_dir/scan_output/gau.txt" "$output_dir/scan_output/waybackurls.txt" "$output_dir/scan_output/subfinder.txt" | sort -u >> "$output_dir/subdomains.txt" || handle_error "Failed to remove duplicates."
print_success "Duplicates removed, subdomains saved to $output_dir/subdomains.txt"

echo ""

# Test for domains running HTTP servers and save to subdomains_http.txt
print_info "Testing for domains running HTTP server"
cat "$output_dir/subdomains.txt" | "httpx" -silent > "$output_dir/subdomains_http.txt" || handle_error "Failed to test for HTTP servers."
print_success "http subdomains saved to $output_dir/subdomains_http.txt"

echo ""
