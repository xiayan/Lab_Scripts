set -o nounset                              # Treat unset variables as an error

showZinc ()
{
    # extract the ZINC ID
    local zincID=`cat $1 | grep ZINC | head -$2 | tail -1 | awk '{print $2}' | sed 's/ZINC\([0-9]*\)_.*/\1/'`

    # copy the ID on clipboard and print the ID in Terminal

    echo $zincID | pbcopy
    echo $zincID

    # open the ZINC webpage in Safari
    open -a Safari http://zinc.docking.org/substance/$zincID
}   # ----------  end of function showZinc  ----------

showZinc $1 $2
