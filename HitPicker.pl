#!/usr/bin/perl -w

print "Enter pdb name: ";
$hitFileName = <STDIN>;
chomp($hitFileName);

unless( open(HITFILE, $hitFileName) ) {
	print "Cannot open file \"$hitFileName\"\n\n";
	exit;
}

@hits = <HITFILE>;
close HITFILE;

$outputfile = "selected_hits.pdb";
unless ( open(SELECTED_HITS, ">$outputfile") ) {
	print "Cannot open file \"$outputfile\" to write to!!\n\n";
}

print "Enter hit numbers (1 line and separated by space):\n";
@hitNumbers = split(/\s+/, <>);

$counter = 0;

foreach (@hits) {
	if ($_ =~ "^COMPND") {
		$counter = $counter + 1;
	}

	if (grep {$_ eq $counter} @hitNumbers) {
		if (!($_ =~ "END")) {
			print SELECTED_HITS $_;
			next;
		} else {
			print SELECTED_HITS $_;
		}
	}
}

close(SELECTED_HITS);

exit;