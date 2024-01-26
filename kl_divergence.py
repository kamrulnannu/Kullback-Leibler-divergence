import math
import sys
import random

def kl_divergence(p, q):
    print("len p %d, len q %d" % (len(p), len(q)))
    if len(p) != len(q):
        raise ValueError("Input distributions must have the same length.")

    kl_sum = 0
    for i in range(len(p)):
        if p[i] != 0 and q[i] != 0:
            kl_sum += p[i] * (math.log2(p[i] / q[i]))

    return kl_sum

def __log__(x, base):
    return math.log(x) / math.log(base)

def create_buckets(data, num_buckets):
    # min_val = min(data)
    min_val = 0.0
    max_val = max(data)
    bucket_size = (max_val - min_val) / num_buckets
    print("Bucket_size: %f" %(bucket_size))

    #buckets = [min_val + i * bucket_size for i in range(num_buckets)] + [max_val]
    buckets = [min_val + i * bucket_size for i in range(num_buckets)]
    buckets.append(max_val + 1e-05)  # Add the exclusive upper bound for the last bucket
    print("sum of bucket values: %f" % (sum(buckets)))

    return buckets

def compute_probability_distribution(data, buckets):
    count = [0] * (len(buckets) - 1)
    for value in data:
        for i in range(len(buckets) - 1):
            if buckets[i] <= value < buckets[i + 1]:
                count[i] += 1
                break

    total = len(data)
    probabilities = [c / total for c in count]
    return probabilities

def compute_exponential_cdf(bucket_boundaries, rate):
    cdf_values = []
    for i in range(len(bucket_boundaries) - 1):
        lower_bound = bucket_boundaries[i]
        upper_bound = bucket_boundaries[i + 1]
        cdf_lower = 1 - math.exp(-rate * lower_bound)
        cdf_upper = 1 - math.exp(-rate * upper_bound)

        # Adjust the last bucket to be treated as an open interval
        if i == len(bucket_boundaries) - 2:
            cdf_upper = 1

        cdf_values.append(cdf_upper - cdf_lower)

    return cdf_values

def ComputeKLDivergence():
    if len(sys.argv) != 3:
        print("Error: Incorrect number of argument(s)")
        print("Usage: %s <number_of_items_in_measured_distributiona> "
              "<number_of_buckets>" % (sys.argv[0]))
        sys.exit(1)

    num_observed_data = int(sys.argv[1])
    num_buckets = int(sys.argv[2])

    latency_data = []
    for i in range(num_observed_data):
        latency_data.append(random.uniform(0.00001, 0.9))

    # Create  buckets
    buckets = create_buckets(latency_data, num_buckets)
    print("buckets value: ")
    print(buckets)

    # Compute measured probability distribution for your data
    measured_prob_distribution = compute_probability_distribution(latency_data, buckets)
    print("msr_dist sum: %f, values:" % (sum(measured_prob_distribution))) 
    print(measured_prob_distribution)

    # Compute exponential distribution parameters
    mean_response_time = sum(latency_data) / len(latency_data)
    rate_parameter = 1 / mean_response_time

    # Compute exponential distribution's CDF values
    exponential_cdf_values = compute_exponential_cdf(buckets, rate_parameter)
    print("exp_dist sum: %f" % (sum(exponential_cdf_values)))
    print(exponential_cdf_values)
    # Compute KL divergence between the measured and exponential distributions
    kl_result = kl_divergence(measured_prob_distribution, exponential_cdf_values)
    print(f"KL Divergence: {kl_result}")

if __name__ == '__main__':
    ComputeKLDivergence()
