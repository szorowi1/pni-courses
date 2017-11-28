%% Add paths.
addpath(genpath('FlySongSegmenter'));
addpath('raw');

%% Change directory. Locate files.
cd('raw');
raw_files = dir('*.abf');

%% Main loop.
for i = 1:length(raw_files)
    
    %% Load file.
    f = raw_files(i).name;
    [d,s,h] = abfload(f);
    
    %% Compute time.
    times = [1e-4:1e-4:length(d)/1e6*s];
    
    %% Run segmenter.
    [data,Sines,Pulses,Params] = FlySongSegmenter(d(:,1),[],[]);
    
    %% Sine Statistics
    % Compute sine carrier frequency (pulled from PlotSegmentation.m).
    region = [1 size(data.d,1)];
    DataFromStart = vertcat(zeros(region(1)-1,1),data.d);
    Sines.LengthCull.clips = GetClips(Sines.LengthCull.start,Sines.LengthCull.stop,DataFromStart);
    sineMFFT = findSineMaxFFT(Sines.LengthCull,data.fs);
    
    % Reassemble into one matrix.
    sineMFFT.freqAll = cellfun(@mean, sineMFFT.freq); %Cheating
    sines = [Sines.LengthCull.start'; Sines.LengthCull.stop'; sineMFFT.freqAll'];
    
    %% Pulse Statistics
    % Compute pulse carrier frequency (pulled from PlotSegmentation.m).
    Pulses.ModelCull2.x = GetClips(Pulses.ModelCull2.w0,Pulses.ModelCull2.w1,DataFromStart);
    pulseMFFT = findPulseMaxFFT(Pulses.ModelCull2,data.fs);
    
    % Reassemble into one matrix.
    pulses = [Pulses.ModelCull2.wc; Pulses.ModelCull2.w0; Pulses.ModelCull2.w1; pulseMFFT.freqAll];
    
    %% Save variables.
    save([f(1:length(f)-4) '.mat'], 'times', 'd', 'sines', 'pulses');    
    clear('d', 'times', 'data', 'Sines', 'Pulses', 'Params', 'sines', 'pulses');
    
end