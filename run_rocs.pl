#!/usr/bin/perl -w
use File::Copy;
use Cwd;

$LIBRARY_LIST = "/home2/labs/karanicolaslab/compounds/zinc_leads_now/multiple/zinc_leads_now_multiple_LIST.txt";
open(LIBRARY, $LIBRARY_LIST) or die("Error: cannot open file '$LIBRARY_LIST'\n");
@lib_list=<LIBRARY>;
close(LIBRARY);

$input_file = $ARGV[0];
open(FILE, $input_file) or die("Error: cannot open file '$input_file'\n");
@lig_list=<FILE>;
close(FILE);

foreach $lig_file (@lig_list){
    chomp($lig_file);
    $lig_tag = $lig_file;
    $lig_tag =~ s/\..*//;
    $mkdir = `mkdir -p $lig_tag`;
    chdir ("$lig_tag") or die("Error: cannot change dir '$folder'\n");
    #$copy = `cp ../$lig_file .`;
	system("cp", "../$lig_file", ".");
    
    foreach $lib_file (@lib_list){
	chomp($lib_file);
	$lib_tag = $lib_file;
	$lib_tag =~ s/\..*//;
		
	print "SUBMITTING...   $lig_tag -:- $lib_tag \n";
	#$rocs = `qsub -v LIG_FILE=$lig_file,LIB_TAG=$lib_tag,LIB_FILE=$lib_file /home2/labs/karanicolaslab/rocs_scripts/rocs.pbs`;
	system("qsub -v", "LIG_FILE=$lig_file,LIB_TAG=$lib_tag,LIB_FILE=$lib_file", "/home2/labs/karanicolaslab/rocs_scripts/rocs.pbs");
    }
    print "\n";
    chdir "..";
}

exit;