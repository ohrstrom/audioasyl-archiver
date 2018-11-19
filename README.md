# Audioasyl - Archiver Tool

Document date:   2018-11-18

The 'Audioasyl Archiver' is a tool built to create a self-containing archive from the
state of the 'legacy' [audioasyl.net](http://audioasyl.net) website.  
'Legacy' refers to the PHP based website version, built around 2010, used until 2018.

The `archiver` combines the data of a mysql-dump and audio-files into a folder-based structure, 
containg audio **and** cleaned up metadata, both in human- and machine-readable formats.  

The resulting archive serves two purposes:
 1. Having a machine-readable dump that can be (at some point of time) imported into the 'new' 
 (resp. 'in-progress') audioasyl.net website.
 2. Having a self-containing archive that can be stored for a long time.  
 It should be possible to - say in 15 years - access & extract the audio- and meta-data without 
 the need of installing a stack of legacy software only to be able to use the data.


### Documentation / Links

- [Documentation](docs/index.md)
- [Repository (GitHub)](https://github.com/ohrstrom/audioasyl-archiver)




