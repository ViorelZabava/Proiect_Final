TARGET=fft
include ../shared/Makefile.shared

$(TARGET): $(TARGET).o
	$(CC) $(TARGET).o -lm $(SNIPER_LDFLAGS) -o $(TARGET)

run_$(TARGET):
	@rm -f results/comparison.txt results/ipc.txt results/time.txt results/power.txt 
	@for param in 1 2 4 8 16 32 64 128 256 512 1024 2048 4096; do \
		echo "Running with parameter $$param"; \
		mkdir -p results/$$param; \
		for run in 1; do \
			echo "Run $$run for parameter $$param"; \
			../../run-sniper -v -n 8 -c gainestown -s Perceptron_predictor:10000:1000:$$param:$$param --power --roi -- ./fft -p 1 > results/$$param/output_run$$run.txt; \
			echo "Parameter: $$param, Run: $$run" >> results/comparison.txt; \
			grep "\[SNIPER\] Elapsed time:" results/$$param/output_run$$run.txt | sed 's/\[SNIPER\] Elapsed time: //' | sed 's/ seconds//' | tee -a results/comparison.txt >> results/time.txt; \
			grep "total" results/$$param/output_run$$run.txt | grep "W" | awk '{print $$2}' | tee -a results/comparison.txt >> results/power.txt; \
			grep "IPC" sim.out | grep -oP '\d+\.\d+' | head -n 1 | tee -a results/comparison.txt >> results/ipc.txt; \
			echo "" >> results/comparison.txt; \
		done; \
	done

CLEAN_EXTRA=viz

