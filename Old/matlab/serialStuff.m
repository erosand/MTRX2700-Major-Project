%%
% Serial testing stuff
clear all; clc;

s1 = serialport("COM1",9600)
s2 = serialport("COM2",9600)


%% Setup
precision = 'uint8';


%% Writing
flush(s1,'output')

msg_out = struct('distance',2.34,'azimuth',15,'elevation',6)


write(s1,msg_out,precision)
writeline(s1,msg_out)


%% Reading
clc
n_ava = s2.NumBytesAvailable
while n_ava
%     data = readline(s2)
    data = read(s2,1,precision)
    n_ava = s2.NumBytesAvailable;
end

%% Parse data

width = 4;
d = dec2bin(data);
n = length(d);
x = [1:width]';
y = [1:n/width]';
x_vec = repmat(x,length(y),1);
y_vec = [];
for i = 1:length(y)
    y_vec = [y_vec;ones(size(x))*y(i)];
end
% pos = zeros(n,2);
% pos(:,1) = x_vec;
% pos(:,2) = y_vec
%%
stock = zeros(1,n);
for i = 1:n
    stock(i) = str2num(d(i));
end
stock








