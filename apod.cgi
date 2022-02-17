#!/usr/local/bin/perl

  #############################################################################
  #                   Copyright (c) 2021 Fritz Feuerbacher.                   #
  #                                                                           #
  #############################################################################
  # This CGI process enables my web pages to get data from HTTP sites when    #
  # my website is hosted using HTTPS.                                         #
  #############################################################################

  $| = 1;  # output NOT buffered
  
  #use strict;
  use warnings;
	
  # Where my FeuerSoft modules reside
  use lib "/home/feuers5/perl5/lib/perl5";  
  use CGI;
    # use Data::Dumper;
  
  binmode(STDOUT, ":utf8");
  
  $ENV{'PERL_LWP_SSL_VERIFY_HOSTNAME'} = 0;
  
  # Print fatal errors to the browser.
  #use CGI::Carp qw(fatalsToBrowser);
  # read the CGI params
  #my $cgi = CGI->new;
  
  use POSIX 'strftime';

  # My NASA token id.
  my $token = "ENTER NASA APOD API KEY HERE";
 
  my $curr_display_date = strftime '%Y-%m-%d', localtime;
  
  my $urlRequest = "https://api.nasa.gov/planetary/apod?api_key=" . $token . "&date=$curr_display_date" . "&hd=true";

  use JSON;
  use JSON::XS qw(decode_json encode_json);
  use Net::SSL;
  use LWP::Simple;
  require LWP::UserAgent;
  require HTTP::Headers;
  use HTTP::Response;
  use HTTP::Request;

  my $ua = LWP::UserAgent->new;
  $ua->timeout(10);
  $ua->env_proxy;
  $ua->max_redirect(0);
  
  my $response = $ua->get($urlRequest);
    
  my $foundNasaApod = "{}";
  
  # Attempt to get the NASA APOD. 
  if (length $response && $response->is_success) {
    $foundNasaApod = $response->content;
  } else {
    # This will substitute if the APOD fails.
    $foundNasaApod = "{\"copyright\":\"Bernard Miller\",\"date\":\"2021-11-12\",\"explanation\":\"The small, northern constellation Triangulum harbors this magnificent face-on spiral galaxy, M33. Its popular names include the Pinwheel Galaxy or just the Triangulum Galaxy. M33 is over 50,000 light-years in diameter, third largest in the Local Group of galaxies after the Andromeda Galaxy (M31), and our own Milky Way. About 3 million light-years from the Milky Way, M33 is itself thought to be a satellite of the Andromeda Galaxy and astronomers in these two galaxies would likely have spectacular views of each other's grand spiral star systems. As for the view from planet Earth, this sharp image shows off M33's blue star clusters and pinkish star forming regions along the galaxy's loosely wound spiral arms. In fact, the cavernous NGC 604 is the brightest star forming region, seen here at about the 4 o'clock position from the galaxy center. Like M31, M33's population of well-measured variable stars have helped make this nearby spiral a cosmic yardstick for establishing the distance scale of the Universe.',\"hdurl\":\"https://apod.nasa.gov/apod/image/2111/M33_PS1_CROP_INSIGHT2048.jpg\",\"media_type\":\"image\",\"service_version\":\"v1\",\"title\":\"M33: The Triangulum Galaxy\",\"url\":\"https://apod.nasa.gov/apod/image/2111/M33_PS1_CROP_INSIGHT1024.jpg\"}";
  }
  
  # Note: this is REQUIRED for the browser to acknowledge response.
  print "Content-type: text/json; charset=utf-8\n\n";
  print $foundNasaApod;
