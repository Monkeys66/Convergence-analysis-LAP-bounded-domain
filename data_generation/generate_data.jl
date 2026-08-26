using Gridap
using GridapGmsh
using LinearAlgebra
using Arpack
using IterativeSolvers
using Printf

model = GmshDiscreteModel(joinpath(@__DIR__, "geo-ellipse.msh"))

order = 1
reffe = ReferenceFE(lagrangian, Float64, order)
V0 = TestFESpace(model, reffe; conformity = :H1, dirichlet_tags = "boundary")

g(x) = 0.0
Ug = TrialFESpace(V0, g)

degree = 2
Ω = Triangulation(model)
dΩ = Measure(Ω, degree)

a1(u, v) = ∫(∇(u) ⋅ ∇(v)) * dΩ
a2(u, v) = ∫(u * v) * dΩ
K = assemble_matrix(a1, Ug, V0)
M = assemble_matrix(a2, Ug, V0)

λ, ϕ = eigs(K, M; nev = 3, which = :SM)

k = sqrt(λ[1])
F(x) = -k * cos(x[1] + x[2])

eig_func = FEFunction(Ug, ϕ[:, 1])
c_1 = sum(∫(F * eig_func) * dΩ)

A = K - k^2 * M
f(v) = ∫(F * v) * dΩ
f_vec = assemble_vector(f, V0)
b = f_vec - c_1 * M * ϕ[:, 1]

u_special_vec = zeros(length(b))
u_special_vec, history = gmres!(
    u_special_vec,
    A,
    b;
    restart = 50,
    maxiter = 25000,
    reltol = 1e-6,
    log = true,
)

a_1 = -c_1 / (2 * k^2)
u_lap_vec = u_special_vec + a_1 * ϕ[:, 1]

# Compute perturbed solutions on the same mesh.
epsilons = [1e-1, 5e-2, 2e-2, 1e-2, 5e-3, 2e-3, 1e-3]
relative_errors = Float64[]

lap_norm = sqrt(real(dot(u_lap_vec, M * u_lap_vec)))

for epsilon in epsilons
    k_epsilon = k + im * epsilon
    A_epsilon = K - k_epsilon^2 * M
    b_epsilon = (k_epsilon / k) * f_vec - c_1 * M * ϕ[:, 1]
    u_epsilon_vec = A_epsilon \ b_epsilon

    difference = u_epsilon_vec - u_lap_vec
    relative_error = sqrt(real(dot(difference, M * difference))) / lap_norm
    push!(relative_errors, relative_error)
end

# Save only epsilon and relative error.
output_path = joinpath(@__DIR__, "ellipse_convergence.csv")
open(output_path, "w") do io
    println(io, "epsilon,relative_error")
    for (epsilon, relative_error) in zip(epsilons, relative_errors)
        @printf(io, "%.16e,%.16e\n", epsilon, relative_error)
    end
end

    
