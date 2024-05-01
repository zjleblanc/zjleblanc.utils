#!/bin/bash

git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
git config user.name "$GITHUB_ACTOR"

#get highest tag number
VERSION=`git describe --abbrev=0 --tags`

if [ $? -eq 1 ] 
then
    exit $?
fi

#replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })

#get number parts and increase last one by 1
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}
VNUM1=`echo $VNUM1 | sed 's/v//'`

# Check for #major or #minor in commit message and increment the relevant version number
MAJOR=`git log --format=%B -n 1 HEAD | grep '#major'`
MINOR=`git log --format=%B -n 1 HEAD | grep '#minor'`

if [ "$MAJOR" ]; then
    echo "Update major version"
    VNUM1=$((VNUM1+1))
    VNUM2=0
    VNUM3=0
elif [ "$MINOR" ]; then
    echo "Update minor version"
    VNUM2=$((VNUM2+1))
    VNUM3=0
else
    echo "Update patch version"
    VNUM3=$((VNUM3+1))
fi


#create new tag
NEW_TAG="v$VNUM1.$VNUM2.$VNUM3"
echo "NEW_VERSION=$VNUM1.$VNUM2.$VNUM3" >> $GITHUB_ENV
echo "Updating $VERSION to $NEW_TAG"

#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT`

#only tag if no tag already
if [ -z "$NEEDS_TAG" ]; then
    echo "Ignoring fatal:cannot describe - this means commit is untagged"
    echo "Tagged with $NEW_TAG"
    git tag $NEW_TAG
    git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git" --tags
else
    echo "Already a tag on this commit"
fi