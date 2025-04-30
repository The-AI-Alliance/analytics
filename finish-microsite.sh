#!/usr/bin/env zsh
#------------------------------------------------------------------------
# Convert this microsite template into your desired microsite.
# Run finish-microsite.sh -h to see the required arguments and options.
# Note: This file defaults to use zsh. If you don't have zsh, but you 
# DO have bash v5+, then use /path/to/bash finish-microsite.sh.
#------------------------------------------------------------------------
set -e

ymdformat="%Y-%m-%d"
tsformat="$ymdformat %H:%M %z"
script=$0
dir=$(dirname $script)
cfg="$dir/docs/_config.yml"
index="$dir/docs/index.markdown" 
work_branch=main
publish_branch=latest
fa_max_number=6  # FAs numbered from 1 to max_...
focus_areas_url="https://thealliance.ai/focus-areas"

declare -A fa_names
fa_names["FA1"]="FA1: Skills and Education"
fa_names["FA2"]="FA2: Trust and Safety"
fa_names["FA3"]="FA3: Applications and Tools"
fa_names["FA4"]="FA4: Hardware Enablement"
fa_names["FA5"]="FA5: Foundation Models and Datasets"
fa_names["FA6"]="FA6: Advocacy"

declare -A fa_url_names
fa_url_names["FA1"]=skills-education
fa_url_names["FA2"]=trust-and-safety
fa_url_names["FA3"]=applications-and-tools
fa_url_names["FA4"]=hardware-enablement
fa_url_names["FA5"]=foundation-models
fa_url_names["FA6"]=advocacy

help() {
	cat << EOF
$script [-h|--help] [-n|--noop] [--ns|--next-steps] \ 
  [--repo-name|-r name] \
  --microsite-title|--site-title|-t title \
  --work-group|-w work_group

Where the options and required arguments are the following:
-h | --help            Print this message and exit.
-n | --noop            Just print the commands but don't run them.
-s | --next-steps      At the end of running this script to create a new repo,
                       some information about "next steps" is printed. If you want to see
                       this information again, run this script again just using this flag.
--repo-name | -r name  The name of GitHub repo. If you are running this script in the 
                       repo's root directory, its name will be used, by default.
--repo-dir | -d name   The absolute path to the repo root directory or the relative
                       path from the current directory. Only needed when you aren't 
                       running this script in the repo root directory.
--work-group-url | -u work_group_url
                       The URL of the work group sponsoring this site.
                       If one of the "FA#" arguments is used for --work-group (see below),
                       then a known URL will be used. If the URL isn't known for the 
                       specified workgroup and one isn't specified, the default URL for 
                       focus areas will be used: $focus_areas_url

These arguments are required, but they can appear in any order. See the example below:

--microsite-title | --site-title | -t title
                       The title of the microsite. 
--work-group | -w work_group
                       The name of work group sponsoring this site.

For example, suppose you want to create a microsite with the title "AI for Evil Project",
under the FA2: Trust and Safety work group, then use the following the command:

$script --repo-name ai-for-evil-project --microsite-title "AI for Evil Project" --work-group fa2

Note that just specifying "fa1" or "FA1", etc. for any of the focus areas will result in the 
following names being used:

EOF

for i in {1..$fa_max_number}
do
	# By "coincidence" it works to use the $focus_areas_url as a prefix!
	printf "%-35s (URL: %s)\n" "${fa_names["FA$i"]}" "${focus_areas_url}/${fa_url_names["FA$i"]}"
done

	cat <<EOF

NOTE: The title and work group strings need to be quoted if they contain spaces!
EOF
}

next_steps() {
	cat << EOF

Next Steps:

Return to the README-template for any additional instructions to follow:

  https://github.com/The-AI-Alliance/microsite-template/blob/main/README-template.md

To see these instructions again, run the following command:

  $script --next-steps
EOF
}

error() {
	for arg in "$@"
	do
		echo "ERROR ($script): $arg"
	done
	echo "ERROR: Try: $script --help"
	exit 1
}

info() {
	for arg in "$@"
	do
		echo "INFO ($script): $arg"
	done
}

repo_dir=
work_group_url=
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--h*)
			help
			exit 0
			;;
		-n|--noop)
			NOOP=echo
			;;
		-s|--next-steps)
			next_steps
			exit 0
			;;
		--repo-name|-r)
			shift
			repo_name="$1"
			;;
		--repo-dir|-d)
			shift
			repo_dir="$1"
			;;
		--microsite-title|--site-title|-t)
			shift
			microsite_title="$1"
			;;
		--work-group|-w)
			shift
			case $1 in				
				fa*|FA*|fA*|Fa*)  # allow all mixes of the case...
					let n=$(echo $1 | sed -e 's/fa//i')
					if [[ $n -ge 1 ]] && [[ $n -le $fa_max_number ]]
					then 
						work_group=${fa_names["FA$n"]}
						[[ -n $work_group_url ]] || work_group_url="${focus_areas_url}/${fa_url_names["FA$n"]}"
					else
						error "Unknown focus area specified: $1. Must be FA1 to FA$fa_max_number"
					fi
					;;
				*)
					work_group="$1"
					[[ -n $work_group_url ]] || work_group_url=$focus_areas_url
					;;
			esac
			;;
		--work-group-url|-u)
			shift
			work_group_url=$1
			;;
		*)
			error "Unrecognized argument: $1"
			;;
	esac
	shift
done

[[ -z "$repo_name" ]] && repo_name=$(basename $PWD)

missing=()
[[ -z "$microsite_title" ]] && missing+=("The microsite title is required. ")
[[ -z "$work_group" ]] && missing+=("The work group name is required. ")
[[ ${#missing[@]} > 0 ]] && error "${missing[@]}"

info "Updating data in the repo:"
info "  Repo name:       $repo_name"
[[ -n "$repo_dir" ]] && \
  info "  Repo dir:        $repo_dir"
info "  Title:           $microsite_title"
info "  Work group:      $work_group"
[[ -n "$work_group_url" ]] && \
  info "  Work group URL:  $work_group_url"

info "Replacing macro placeholders with values:"
[[ -z "$ymdtimestamp" ]] && ymdtimestamp=$(date +"$ymdformat")
date -j -f "$ymdformat" +"$ymdformat" "$ymdtimestamp" > /dev/null 2>&1
[[ $? -ne 0 ]] && error "Invalid YMD timestamp format for timestamp: $ymdtimestamp" "Required format: $ymdformat"
[[ -z "$timestamp" ]] && timestamp=$(date +"$tsformat")
date -j -f "$tsformat" +"$tsformat" "$timestamp" > /dev/null 2>&1
[[ $? -ne 0 ]] && error "Invalid timestamp format for timestamp: $timestamp" "Required format: $tsformat"

[[ -n "$repo_dir" ]] && $NOOP cd "$repo_dir"

files=(
	Makefile
	README.md
	publish-website.sh
	update-main.sh
	docs/_config.yml
)
markdown_files=($(find docs -name '*.markdown'))
html_files=($(find docs/_layouts -name '*.html'))

info "Replacing macros with correct values:"
info "  REPO_NAME:       $repo_name"
info "  MICROSITE_TITLE: $microsite_title"
info "  WORK_GROUP_NAME: $work_group"
info "  WORK_GROUP_URL:  $work_group_url"
info "  YMD_TSTAMP:      $ymdtimestamp"
info "  TIMESTAMP:       $timestamp"
info
info "Processing Files:"

for file in "${files[@]}" "${markdown_files[@]}" "${html_files[@]}"
do
	info "  $file"
	if [[ -z $NOOP ]]
	then 
		sed -e "s?REPO_NAME?$repo_name?g" \
		    -e "s?MICROSITE_TITLE?$microsite_title?g" \
		    -e "s?WORK_GROUP_NAME?$work_group?g" \
		    -e "s?WORK_GROUP_URL?$work_group_url?g" \
		    -e "s?YMD_TSTAMP?$ymdtimestamp?g" \
		    -e "s?TIMESTAMP?$timestamp?g" \
		    -i ".back" "$file"
	else
		$NOOP sed ... -i .back $file
	fi
done

info "Delete the backup '*.back' files that were just made."
$NOOP find . -name '*.back' -exec rm {} \;

info "Committing changes to the main branch."
# Use --no-verify to suppress complaints and nonzero exit when
# there is nothing to commit.
$NOOP git commit --no-verify -m "$0: Committing changes after variable substitution." .

exists=$(git br -a | grep latest | wc -l)
if [[ $exists -eq 0 ]]
then
	info "Create a 'latest' branch, from which the pages will be published."
	$NOOP git checkout -b latest
else
	info "Merge the changes to the 'latest' branch, from which the pages will be published."
	$NOOP git checkout latest
	$NOOP git merge main
	$NOOP git commit --no-verify -m 'update publication branch, latest, from main branch' .
fi

info "Switching back to the main branch."
$NOOP git checkout main

info "Done! The current working directory is $PWD."
next_steps
